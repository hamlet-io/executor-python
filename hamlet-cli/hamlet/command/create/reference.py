import click
from hamlet.backend.create import reference as create_reference_backend


@click.command(
    'reference',
    short_help='Create a Codeontap Component Reference',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-t',
    '--reference-type',
    required=True,
    help='type of object you need the reference for'
)
@click.option(
    '-o',
    '--reference-output-dir',
    help='output directory',
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True
    )
)
def reference(**kwargs):
    """
    Create a Codeontap Component Reference
    """
    create_reference_backend.run(**kwargs, _is_cli=True)
