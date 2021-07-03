import os
import base64
import tempfile
import hashlib
import shutil
import httpx
import typing
import www_authenticate

from urllib import parse


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
        realm_client = httpx.Client()

        if self.username or self.password:
            realm_client.headers["Authorization"] = self._build_basic_auth_header(
                username, password
            )

        realm_response = realm_client.get(
            self._build_realm_token_url(registry_response, repository, actions)
        ).json()
        realm_token = realm_response.get("access_token") or realm_response["token"]

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
    def __init__(self, registry_url, repository, username=None, password=None) -> None:

        self.registry_url = registry_url
        self.repository = repository

        self.username = username
        self.password = password

        self.registry_client = httpx.Client(
            base_url=self.registry_url,
            auth=DockerRegistryV2Auth(self.repository, self.username, self.password),
            headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"},
        )

    @property
    def tags(self):
        return self.registry_client.get(f"/v2/{self.repository}/tags/list").json()[
            "tags"
        ]

    def get_tag_digest(self, tag):
        return self.get_tag_manifest(tag)["config"]["digest"]

    def get_tag_manifest(self, tag):
        manifest_response = self.registry_client.get(
            f"/v2/{self.repository}/manifests/{tag}"
        )

        try:
            manifest_response.raise_for_status()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.NOT_FOUND:
                raise ContainerTagNotFoundException(self.repository, tag, e)

            raise e

        return manifest_response.json()

    def pull(self, tag, dst_dir):
        manifest = self.get_tag_manifest(tag)

        with tempfile.TemporaryDirectory() as extract_dir:
            with tempfile.TemporaryDirectory() as stage_dir:
                for layer in manifest["layers"]:
                    with tempfile.NamedTemporaryFile(
                        dir=stage_dir, delete=False
                    ) as layer_file:

                        layer_url = self.registry_client.get(
                            url=f'/v2/{self.repository}/blobs/{layer["digest"]}',
                            allow_redirects=True,
                        ).url

                        with self.registry_client.stream(
                            method="get", url=layer_url
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

                        if (
                            layer["mediaType"]
                            == "application/vnd.docker.image.rootfs.diff.tar.gzip"
                        ):

                            shutil.unpack_archive(layer_file.name, extract_dir, "gztar")

                if os.listdir(extract_dir):
                    if os.path.isdir(dst_dir):
                        shutil.rmtree(dst_dir)
                    shutil.copytree(extract_dir, dst_dir, symlinks=True)

        return manifest
