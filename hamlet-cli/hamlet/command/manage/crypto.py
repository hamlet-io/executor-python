import click
from hamlet.backend.manage import crypto as manage_crypto_backend
from hamlet.command.common.config import pass_options
from hamlet.command.common import exceptions


@click.command(
    'crypto',
    short_help='Manage cryptographic operations using KMS',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-a',
    '--alias',
    help='alias for the master key to be used'
)
@click.option(
    '-b',
    '--base64-decode',
    is_flag=True,
    help='force base64 decode of the input before processing'
)
@click.option(
    '-d',
    '--decrypt',
    is_flag=True,
    help='decrypt operation'
)
@click.option(
    '-e',
    '--encrypt',
    is_flag=True,
    help='encrypt operation'
)
@click.option(
    '-f',
    '--crypto-file',
    help='file which contains the plaintext or ciphertext to be processed',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    )
)
@click.option(
    '-k',
    '--key-id',
    help='master key to be used'
)
@click.option(
    '-n',
    '--no-alteration',
    help='no alteration to CRYPTO_TEXT (pass through as is)',
    is_flag=True
)
@click.option(
    '-p',
    '--json-path',
    help='path to the attribute within CRYPTO_FILE to be processed'
)
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    help="don't display result(quiet)"
)
@click.option(
    '-t',
    '--crypto-text',
    help='plaintext or ciphertext to be processed'
)
@click.option(
    '-u',
    '--update',
    is_flag=True,
    help='update the attribute at JSON_PATH (if provided), or replace CRYPTO_FILE with operation result'
)
@click.option(
    '-v',
    '--visible',
    help='result is base64 decoded (visible)',
    is_flag=True
)
@exceptions.backend_handler()
@pass_options
def crypto(options, **kwargs):
    """
    Manage cryptographic operations using KMS

    \b
    NOTES:
    1. If a file is required but not provided, the default filename
         will be expected in the equivalent directory of the infrastructure tree
    2. If JSON_PATH is provided,
       - a CRYPTO_FILE is required
       - the targetted file must be JSON format
       - encrypt requires CRYPTO_TEXT to be provided, or for the attribute to
         to present
       - attribute is updated with the operation result if update flag is set
    3. If JSON_PATH is NOT provided,
       - one of CRYPTO_FILE or CRYPTO_TEXT must be provided
       - CRYPTO_TEXT takes precedence over CRYPTO_FILE
    4. If a file at CRYPTO_FILE can't be located based on current directory, it will be
       treated as a relative directory using the default filename
    5. Don't include "alias/" in any provided alias
    6. If encrypting, the key is located as follows,
       - use KEYID if provided
       - use ALIAS if provided
       - if in segment directory, use segment keyid if available
       - if in product directory, use product keyid if available
       - if in account directory, use account keyid if available
       - otherwise error
    7. The result is sent to stdout and is base64 encoded unless the
       visibility flag is set
    8. Decrypted files will have a ".decrypted" extension added so they can be ignored by git
    """

    args = {
        **options.opts,
        **kwargs
    }

    manage_crypto_backend.run(**args, _is_cli=True)
