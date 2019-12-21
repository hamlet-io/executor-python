import os
import click
from cot.backend.test.generate import run as test_generate_backend


@click.command(
    'generate',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-f',
    '--filename',
    'filenames',
    multiple=True,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        exists=True
    )
)
@click.option(
    '-d',
    '--directory',
    'directory',
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=True
    )
)
@click.option(
    '-o',
    '--output',
    'output',
    type=click.Path(
        file_okay=True,
        dir_okay=False
    )
)
def geneate(
    filenames,
    output,
    directory
):
    if not filenames and not directory:
        directory = os.getcwd()
    result = test_generate_backend(
        filenames=filenames,
        output=output,
        directory=directory
    )
    if not output:
        click.echo(result)
