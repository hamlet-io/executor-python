import os
import shutil
import tempfile
from configparser import ConfigParser
from hamlet.backend.common.runner import run as script_run


def run(
    ScriptFilePath=None,
    AWSRegion=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Run a bash script with the AWS Cli console configured
    for a provided account
    Outputs piped to HAMLET_OUTPUTS as key=value returned as outputs
    """

    with tempfile.NamedTemporaryFile() as output_file:
        env["AWS_ACCESS_KEY_ID"] = AWSAccessKeyId
        env["AWS_SECRET_ACCESS_KEY"] = AWSSecretAccessKey
        env["AWS_SESSION_TOKEN"] = AWSSessionToken
        env["AWS_DEFAULT_REGION"] = AWSRegion
        env["AWS_CLI_BASH_SCRIPT_DIR"] = os.path.dirname(ScriptFilePath)
        env["HAMLET_OUTPUTS"] = output_file.name

        try:
            del env["AWS_SECURITY_TOKEN"]
        except NameError:
            pass
        try:
            del env["AWS_PROFILE"]
        except NameError:
            pass

        if shutil.which("aws") is None:
            raise Exception(
                (
                    "aws command not found on path install from"
                    "https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
                )
            )

        script_run(
            script_name=os.path.basename(ScriptFilePath),
            script_base_path_env="AWS_CLI_BASH_SCRIPT_DIR",
            env=env,
            _is_cli=True,
        )

        config = ConfigParser(strict=False)
        s_config = open(output_file.name, "r").read()
        s_config = f"[ini]\n{s_config}"

        config.read_string(s_config)

        outputs = {}
        items = config.items("ini")
        for key, value in items:
            outputs[key] = value

    return {"Properties": {"Outputs": outputs}}
