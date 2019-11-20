import click
from cot.backend.manage import file_crypto as manage_file_crypto_backend


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
def file_crypto(**kwargs):
    """
    Manage crypto for files

    \b
    NOTES:
    1. If no operation is provided, the current file contents are displayed
    """
    manage_file_crypto_backend.run(**kwargs)
