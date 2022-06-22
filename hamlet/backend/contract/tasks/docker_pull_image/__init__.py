from hamlet.backend.common.exceptions import BackendException

import docker
import docker.errors


def run(Image, env={}):
    """
    pull a docker image to the local docker host
    """

    client = docker.from_env()

    try:
        client.ping()
    except docker.errors.APIError as e:
        raise BackendException(str(e))

    try:
        client.images.pull(repository=Image, all_tags=False)
    except docker.errors.NotFound as e:
        raise BackendException(str(e))

    return {"Properties": {}}
