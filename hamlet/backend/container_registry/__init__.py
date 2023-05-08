import os
import base64
import tempfile
import hashlib
import shutil
import httpx
import typing
import www_authenticate
import json

from hamlet.backend.common.http_client import HTTPClient

from urllib import parse

container_httpx_client = HTTPClient(
    headers={
        "Accept": ", ".join(
            [
                "application/vnd.oci.image.index.v1+json",
                "application/vnd.oci.image.manifest.v1+json",
                "application/vnd.docker.distribution.manifest.v2+json",
            ]
        )
    }
)

auth_httpx_client = HTTPClient()


class ContainerRepositoryException(BaseException):
    def __init__(self, repository: str, *args: object) -> None:
        self.repository = repository
        super().__init__(*args)


class ContainerTagNotFoundException(ContainerRepositoryException):
    def __init__(self, repository: str, tag: str, *args: object) -> None:
        self.tag = tag
        super().__init__(repository, *args)


class DockerRegistryV2Auth(httpx.Auth):
    def __init__(self, repository, username=None, password=None) -> None:
        self.repository = repository
        self.username = username
        self.password = password
        self.token = None

    actions = ["pull"]

    def auth_flow(
        self, request: httpx.Request
    ) -> typing.Generator[httpx.Request, httpx.Response, None]:
        if self.token:
            request.headers["Authorization"] = self.token

        response = yield request

        if response.status_code == httpx.codes.UNAUTHORIZED:
            self.token = self.sign_request(
                response, self.repository, self.actions, self.username, self.password
            )
            request.headers["Authorization"] = self.token

            yield request

    def sign_request(
        self, registry_response, repository, actions, username, password
    ) -> str:
        if self.username or self.password:
            auth_httpx_client.headers["Authorization"] = self._build_basic_auth_header(
                username, password
            )

        realm_response = auth_httpx_client.get(
            self._build_realm_token_url(registry_response, repository, actions)
        )

        try:
            realm_response.raise_for_status()
        except httpx.HTTPError as e:
            raise e

        realm_token = json.loads(realm_response.text).get("access_token") or json.loads(
            realm_response.text
        ).get("token")
        return f"Bearer {realm_token}"

    def _build_basic_auth_header(self, username, password) -> str:
        userpass = b":".join((httpx.to_bytes(username), httpx.to_bytes(password)))
        token = base64.b64encode(userpass).decode()
        return f"Basic {token}"

    def _build_realm_token_url(self, response, repository, actions) -> str:
        www_authenticate_response = www_authenticate.parse(
            response.headers["WWW-Authenticate"]
        )

        if "bearer" in www_authenticate_response:
            if self.actions:
                scope = f"repository:{repository}:" + ",".join(actions)
            elif "scope" in www_authenticate_response["bearer"]:
                scope = www_authenticate_response["bearer"]["scope"]
            else:
                scope = ""

            url_parts = list(
                parse.urlparse(www_authenticate_response["bearer"]["realm"])
            )
            query = parse.parse_qs(url_parts[4])
            query.update(
                {
                    "service": www_authenticate_response["bearer"]["service"],
                    "scope": scope,
                }
            )
            url_parts[4] = parse.urlencode(query, True)
            url_parts[0] = "https"

            return parse.urlunparse(url_parts)


class ContainerRepository:
    def __init__(
        self,
        registry_url,
        repository,
        username=None,
        password=None,
        architecture="amd64",
        os="linux",
    ) -> None:
        self.registry_url = registry_url
        self.repository = repository

        self.username = username
        self.password = password

        self.auth_token = DockerRegistryV2Auth(
            self.repository, self.username, self.password
        )

        self.architecture = architecture
        self.os = os

    @property
    def tags(self):
        tags = []
        query_params = {"n": 20}
        links_complete = False

        while True:
            tag_response = container_httpx_client.get(
                f"{self.registry_url}/v2/{self.repository}/tags/list",
                params=query_params,
                auth=self.auth_token,
            )
            try:
                tag_response.raise_for_status()
            except httpx.HTTPError as e:
                raise e

            link = tag_response.headers.get("Link", None)
            if link is not None:
                query_params = parse.urlparse(
                    (link.split(";")[0]).strip("<").rstrip(">")
                ).query
            else:
                links_complete = True

            tags += json.loads(tag_response.text).get("tags")

            if links_complete:
                break

        return tags

    def get_tag_digest(self, tag):
        return self.get_tag_manifest(tag).headers["docker-content-digest"]

    def get_tag_manifest(self, tag):
        manifest_response = container_httpx_client.get(
            f"{self.registry_url}/v2/{self.repository}/manifests/{tag}",
            auth=self.auth_token,
        )

        try:
            manifest_response.raise_for_status()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.NOT_FOUND:
                raise ContainerTagNotFoundException(self.repository, tag, e)
            raise e

        # Handle support for Image Indexes
        # https://github.com/opencontainers/image-spec/blob/main/image-index.md
        if (
            manifest_response.json().get("mediaType")
            == "application/vnd.oci.image.index.v1+json"
        ):
            listed_manifest_entry = next(
                iter(
                    [
                        manifest
                        for manifest in manifest_response.json()["manifests"]
                        if manifest["platform"]["architecture"] == self.architecture
                        and manifest["platform"]["os"] == self.os
                    ]
                ),
                None,
            )

            if listed_manifest_entry is None:
                raise ContainerTagNotFoundException(
                    self.repository,
                    tag,
                    f"No manifest for platform {self.os}/{self.architecture}",
                )

            manifest_response = container_httpx_client.get(
                f"{self.registry_url}/v2/{self.repository}/manifests/{listed_manifest_entry['digest']}",
                auth=self.auth_token,
            )

            try:
                manifest_response.raise_for_status()

            except httpx.HTTPStatusError as e:
                if e.response.status_code == httpx.codes.NOT_FOUND:
                    raise ContainerTagNotFoundException(self.repository, tag, e)
                raise e

        return manifest_response

    def pull(self, tag, dst_dir):
        manifest_response = self.get_tag_manifest(tag)
        manifest = manifest_response.json()

        with tempfile.TemporaryDirectory() as extract_dir:
            with tempfile.TemporaryDirectory() as stage_dir:
                for layer in manifest["layers"]:
                    with tempfile.NamedTemporaryFile(
                        dir=stage_dir, delete=False
                    ) as layer_file:
                        layer_blob = container_httpx_client.get(
                            url=f'{self.registry_url}/v2/{self.repository}/blobs/{layer["digest"]}',
                            auth=self.auth_token,
                        )

                        try:
                            layer_blob.raise_for_status()
                        except httpx.HTTPError as e:
                            raise e

                        with container_httpx_client.stream(
                            method="get",
                            url=layer_blob.url,
                            auth=self.auth_token,
                        ) as r:
                            for chunk in r.iter_raw(chunk_size=(1024 * 1024 * 3)):
                                layer_file.write(chunk)

                        layer_file.flush()

                        digest_algorithm = layer["digest"].split(":")[0]
                        digest_hash = layer["digest"].split(":")[1]

                        file_hash = hashlib.new(digest_algorithm)
                        with open(layer_file.name, "rb") as f:
                            for byte_block in iter(
                                lambda: f.read((1024 * 1024 * 10)), b""
                            ):
                                file_hash.update(byte_block)

                        if digest_hash != file_hash.hexdigest():
                            print(
                                (
                                    "Layer hash does not match digest "
                                    f"- ours {file_hash.hexdigest()} - theirs {digest_hash}"
                                )
                            )

                        if layer["mediaType"] in [
                            "application/vnd.docker.image.rootfs.diff.tar.gzip",
                            "application/vnd.oci.image.layer.v1.tar+gzip",
                        ]:
                            shutil.unpack_archive(layer_file.name, extract_dir, "gztar")

                        elif layer["mediaType"] in [
                            "application/vnd.oci.image.layer.v1.tar"
                        ]:
                            shutil.unpack_archive(layer_file.name, extract_dir, "tar")

                if os.listdir(extract_dir):
                    if os.path.isdir(dst_dir):
                        shutil.rmtree(dst_dir)
                    shutil.copytree(extract_dir, dst_dir, symlinks=True)

        return manifest_response.headers["docker-content-digest"]
