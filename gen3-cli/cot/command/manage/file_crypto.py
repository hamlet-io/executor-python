import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'file-crypto',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-d',
    '--decrypt',
    is_flag=True,
    help='decrypt file'
)
@click.option(
    '-e',
    '--encrypt',
    is_flag=True,
    help='encrypt file'
)
@click.option(
    '-f',
    '--crypto-file',
    help='path to the file managed'
)
@click.option(
    '-u',
    '--update',
    is_flag=True,
    help='update the file'
)
def file_crypto(
    decrypt,
    encrypt,
    crypto_file,
    update
):
    """
    Manage crypto for files

    \b
    NOTES:
    1. If no operation is provided, the current file contents are displayed
    """
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
