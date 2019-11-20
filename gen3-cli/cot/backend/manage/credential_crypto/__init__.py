import subprocess
from cot import utils
from cot import env


def run(
    credential_email=None,
    crypto_file=None,
    credential_id=None,
    credential_path=None,
    credential_secret=None,
    visible=None,
    credential_type=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'manageCredentialCrypto.sh',
        options={
            '-e': credential_email,
            '-f': crypto_file,
            '-i': credential_id,
            '-n': credential_path,
            '-v': visible,
            '-y': credential_type,
            '-s': credential_secret
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
