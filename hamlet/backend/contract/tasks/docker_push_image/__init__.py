from hamlet.backend.common.exceptions import BackendException

import docker
import docker.errors


def run(SourceImage, DestinationImage, env={}):
    """
    push a docker image from the local docker host to a remote registry
    """

    client = docker.from_env()

    try:
        client.ping()
    except docker.errors.APIError as e:
        raise BackendException(str(e))

    try:
        source_image = client.images.get(SourceImage)

    except docker.errors.NotFound as e:
        raise BackendException(str(e))

    source_image.tag(DestinationImage)
    source_image.reload()
    client.images.push(DestinationImage)

    try:
        client.images.get_registry_data(DestinationImage)
    except docker.errors.NotFound as e:
        raise BackendException(str(e))

    return {
        "Properties": {
            "source_image": SourceImage,
            "destination_image": DestinationImage,
        }
    }
