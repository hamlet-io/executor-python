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
    required=True,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
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
    output
):
    result = test_generate_backend(filenames, output)
    if not output:
        click.echo(result)
