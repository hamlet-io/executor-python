import os

import boto3
import botocore.session
from botocore import credentials

# Use the cli cache so that we can run aws commands and boto commands with the same creds
cli_cache = os.path.join(os.path.expanduser("~"), ".aws/cli/cache")


def boto3_session(
    profile_name=None, config_file=None, credentials_file=None, existing_creds=None
):
    """
    returns a boto3 session using cached credentials
    Allows for sharing credentials from cli commands with boto sessions
    """
    # Construct botocore session with cache
    session = botocore.session.get_session()

    if profile_name is not None:
        session.set_config_variable("profile", profile_name)

    if config_file is not None:
        session.set_config_variable("config_file", config_file)

    if credentials_file is not None:
        session.set_config_variable("credentials_file", credentials_file)

    if existing_creds is not None:
        session.set_credentials(
            access_key=existing_creds["aws_access_key_id"],
            secret_key=existing_creds["aws_secret_access_key"],
            token=existing_creds["aws_session_token"],
        )

    session.get_component("credential_provider").get_provider(
        "assume-role"
    ).cache = credentials.JSONFileCache(cli_cache)

    return boto3.Session(botocore_session=session)
