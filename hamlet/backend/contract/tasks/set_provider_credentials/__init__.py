import tempfile
from configparser import ConfigParser

from hamlet.backend.common import aws_credentials_session, runner


def run(AccountId, ProviderId, Provider, env={}):
    """
    Uses the standard hamlet credentials process to determine the
    authentication for this call

    For AWS collect the temporary credentials from an assume role and return
    as a credential set
    """

    cred_result = {}

    with tempfile.NamedTemporaryFile() as output_file:
        env = {
            **env,
            "CRED_ACCOUNT": AccountId,
            "PROVIDERID": ProviderId,
            "ACCOUNT_PROVIDER": Provider,
        }
        runner.run(
            "execution/setCredentials.sh",
            args=[],
            options={},
            env=env,
            engine=None,
            _is_cli=True,
            script_base_path_env="GENERATION_BASE_DIR",
            extra_script=f"&&  env | grep 'AWS' > {output_file.name}",
        )

        config = ConfigParser(strict=False)

        s_config = open(output_file.name, "r").read()
        s_config = f"[ini]\n{s_config}"

        config.read_string(s_config)
        items = config.items("ini")
        for key, value in items:
            cred_result[key] = value

        existing_creds = None

        if cred_result.get("aws_access_key_id", None) is not None:
            existing_creds = {
                "aws_access_key_id": cred_result["aws_access_key_id"],
                "aws_secret_access_key": cred_result["aws_secret_access_key"],
                "aws_session_token": cred_result.get("aws_Session_token", None),
            }

        credentials = aws_credentials_session.boto3_session(
            profile_name=cred_result.get("aws_profile", None),
            config_file=cred_result.get("aws_config_file", None),
            credentials_file=cred_result.get("aws_shared_credentials_file", None),
            existing_creds=existing_creds,
        ).get_credentials()

        try:
            credentials = credentials.get_frozen_credentials()

        except AttributeError:
            pass

    return {
        "Properties": {
            "aws_access_key_id": credentials.access_key,
            "aws_secret_access_key": credentials.secret_key,
            "aws_session_token": credentials.token,
        }
    }
