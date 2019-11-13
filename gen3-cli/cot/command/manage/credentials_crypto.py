import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'credential-crypto',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-e',
    '--credential-email',
    help='email associated with the credential (not encrypted)'
)
@click.option(
    '-f',
    '--crypto-file',
    help='path to the credentials file to be used',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    )
)
@click.option(
    '-i',
    '--credential-id',
    help='id of credential (i.e. Username/Client Key/Access Key value) - not encrypted'
)
@click.option(
    '-n',
    '--credential-path',
    help='path for the set of values (id, secret, email)',
    required=True
)
@click.option(
    '-s',
    '--credential-secret',
    help='secret of credential (i.e. Password/Secret Key value) - encrypted'
)
@click.option(
    '-v',
    '--visible',
    help='if credential secret should be decrypted (visible)',
    is_flag=True
)
@click.option(
    '-y',
    '--credential-type',
    help='type of credential',
    required=True,
    type=click.Choice(
        [
            'login',
            'api',
            'env'
        ],
        case_sensitive=False
    ),
    default='login',
    show_default=True
)
def credentials_crypto(
    credential_email,
    crypto_file,
    credential_id,
    credential_path,
    credential_secret,
    visible,
    credential_type
):
    """
    Manage crypto for credential storage

    \b
    NOTES:
    1. CREDENTIAL_PATH is a JSON path so values separated by dots. It is case sensitive.
    2. CREDENTIAL_TYPE is ${CREDENTIAL_TYPE_LOGIN}, ${CREDENTIAL_TYPE_API} or ${CREDENTIAL_TYPE_ENV}
    3. For CREDENTIAL_TYPE of ${CREDENTIAL_TYPE_LOGIN}, Id Attribute = Username, Secret Attribute = Password
    4. For CREDENTIAL_TYPE of ${CREDENTIAL_TYPE_API}, Id Attribute = AccessKey, Secret Attribute = SecretKey
    5. For CREDENTIAL_TYPE of ${CREDENTIAL_TYPE_ENV}, Id Attribute = ACCESS_KEY, Secret Attribute = SECRET_KEY
    """
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
