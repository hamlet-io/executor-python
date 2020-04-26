import click
from hamlet.backend.create import unitlist as create_unitlist_backend


@click.command(
    'unitlist',
    short_help='Create a unitlist output of the segment',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-i',
    '--generation-input-source',
    help='source of input data to use when generating the template'
)
@click.option(
    '-o',
    '--output-dir',
    help='the directory where the outputs will be saved. Mandatory when Input Source set to Mock.'
)
@click.option(
    '-p',
    '--generation-provider',
    help='provider to for template generation',
    default='aws',
    show_default=True
)
@click.option(
    '-f',
    '--generation-framework',
    help='output framework to use for template generation',
    default='cf',
    show_default=True
)
def unitlist(**kwargs):
    """
    Create a unit list output of the segment

    \b
    NOTES:

    1. You must be in the directory specific to the level
    """
    create_unitlist_backend.run(**kwargs, _is_cli=True)
