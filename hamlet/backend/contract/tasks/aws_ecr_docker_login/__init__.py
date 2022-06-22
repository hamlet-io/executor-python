from hamlet.backend.common.exceptions import BackendException
from base64 import b64decode

import boto3
import docker
import docker.errors


def run(
    RegistryId=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Perform a docker login for an AWS ECR Registry
    """

    docker_client = docker.from_env()

    try:
        docker_client.ping()
    except docker.errors.APIError as e:
        raise BackendException(str(e))

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )
    ecr = session.client("ecr")

    auth_token_args = {}
    if RegistryId:
        auth_token_args["registryIds"] = [RegistryId]

    auth_token_response = ecr.get_authorization_token(**auth_token_args)

    auth_token = auth_token_response["authorizationData"][0]

    ecr_password = (
        b64decode(auth_token["authorizationToken"])
        .replace(b"AWS:", b"")
        .decode("utf-8")
    )

    try:
        docker_client.login(
            username="AWS", password=ecr_password, registry=auth_token["proxyEndpoint"]
        )

    except docker.errors.APIError as e:
        raise BackendException(str(e))

    docker_client.ping()

    return {"Properties": {"registry": auth_token["proxyEndpoint"]}}
