import os
import base64
import requests
import tempfile
import hashlib
import shutil

import www_authenticate

from urllib import parse


def get_registry_login_token(
        registry_url,
        repository, actions=['pull'],
        username=None,
        password=None,
        authorization_header=None
):
    '''
    Uses the docker v2 registry api to get an auth token compliant with the registry
    '''
    registry_base_url = parse.urljoin(registry_url, 'v2/')
    registry_version = requests.get(registry_base_url, allow_redirects=True)

    if registry_version.status_code == requests.codes.ok:
        return None

    if registry_version.status_code != requests.codes.unauthorized:
        raise requests.exceptions.HTTPError(registry_version)

    if registry_version.status_code == requests.codes.unauthorized:

        if username is not None and password is not None:
            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f'{username}:{password}').decode('utf-8')
            }

        elif authorization_header is not None:
            headers = {
                'Authorization': authorization_header
            }
        else:
            headers = {}

        status_respose = www_authenticate.parse(registry_version.headers['WWW-Authenticate'])

        if 'bearer' in status_respose:
            bearer_info = status_respose['bearer']
            if actions:
                scope = f'repository:{repository}:' + ','.join(actions)
            elif 'scope' in bearer_info:
                scope = bearer_info['scope']
            else:
                scope = ''
            url_parts = list(parse.urlparse(bearer_info['realm']))
            query = parse.parse_qs(url_parts[4])
            query.update({
                'service': bearer_info['service'],
                'scope': scope
            })
            url_parts[4] = parse.urlencode(query, True)
            url_parts[0] = 'https'
            auth_url = parse.urlunparse(url_parts)

            auth_response = requests.get(auth_url, headers=headers)
            auth_response.raise_for_status()

            auth_json = auth_response.json()

            return auth_json.get('access_token') or auth_json['token']

    return None


def get_registry_image_manifest(registry_url, repository, tag, auth_token):
    '''
    Get the manifest of a docker image based on the v2 docker registry spec
    The manifest contains the layers and details of the over all docker image
    '''
    manifest_url = parse.urljoin(registry_url, f'v2/{repository}/manifests/{tag}')
    if auth_token is not None:
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Accept': 'application/vnd.docker.distribution.manifest.v2+json'
        }
    else:
        headers = {}

    manifest_response = requests.get(manifest_url, headers=headers, allow_redirects=True)
    manifest_response.raise_for_status()

    return manifest_response.json()


def pull_registry_image_to_dir(registry_url, repository, manifest, auth_token, dest_dir):
    '''
    Pull down all of the layers from a manifest and extract the tars over the top of each other
    This is what docker itself does we are just using the docker images as file sharing rather than an container
    '''
    blob_base_url = parse.urljoin(registry_url, f'/v2/{repository}/blobs/')
    if auth_token is not None:
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
    else:
        headers = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        extract_dir = os.path.join(temp_dir, 'extract')
        os.makedirs(extract_dir)

        for layer in manifest['layers']:
            with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as layer_file:
                layer_url = blob_base_url + layer['digest']

                layer_response = requests.get(layer_url, headers=headers, allow_redirects=True)
                layer_response.raise_for_status()
                layer_content = requests.get(layer_response.url, stream=True, headers=headers)
                layer_content.raise_for_status()

                for chunk in layer_content.iter_content(chunk_size=(1024 * 1024)):
                    if chunk:
                        layer_file.write(chunk)

                layer_file.flush()

                digest_algorithm = layer['digest'].split(':')[0]
                digest_hash = layer['digest'].split(':')[1]

                file_hash = hashlib.new(digest_algorithm)
                with open(layer_file.name, "rb") as f:
                    for byte_block in iter(lambda: f.read((1024 * 1024)), b""):
                        file_hash.update(byte_block)

                if digest_hash != file_hash.hexdigest():
                    print(f'Layer hash does not match digest - ours {file_hash.hexdigest()} - theirs {digest_hash}')

                if layer['mediaType'] == 'application/vnd.docker.image.rootfs.diff.tar.gzip':

                    shutil.unpack_archive(layer_file.name, extract_dir, 'gztar')

        if os.listdir(extract_dir):
            if os.path.isdir(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(extract_dir, dest_dir, symlinks=True)
