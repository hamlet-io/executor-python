import subprocess
from cot import utils
from cot import env


def run(
    decrypt=None,
    encrypt=None,
    crypto_file=None,
    update=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'manageFileCrypto.sh',
        options={
            '-d': decrypt,
            '-e': encrypt,
            '-f': crypto_file,
            '-u': update
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
