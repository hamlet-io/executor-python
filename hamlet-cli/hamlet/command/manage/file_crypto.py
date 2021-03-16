import click
from hamlet.backend.manage import file_crypto as manage_file_crypto_backend
from hamlet.backend.common.exceptions import BackendException
from hamlet.command.common.exceptions import CommandError
from hamlet.command.common.config import pass_options

@click.command(
    'file-crypto',
    short_help='Manage crypto for files',
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
    help='path to the file managed',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    )
)
@click.option(
    '-u',
    '--update',
    is_flag=True,
    help='update the file'
)
@pass_options
def file_crypto(options, **kwargs):
    """
    Manage crypto for files

    \b
    NOTES:
    1. If no operation is provided, the current file contents are displayed
    """

    args = {
        **options.opts,
        **kwargs
    }

    try:
        manage_file_crypto_backend.run(**args, _is_cli=True)
    except BackendException as e:
        raise CommandError(str(e))
