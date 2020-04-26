import click
from cot.backend.create import buildblueprint as create_buildblueprint_backend


@click.command(
    'build-blueprint',
    short_help='Create a blueprint output for the provided deployment unit',
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
@click.option(
    '-u',
    '--deployment-unit',
    help='deployment unit to be included in the template',
    required=True
)
def buildblueprint(**kwargs):
    """
    Create a blueprint output for the provided deployment unit

    \b
    NOTES:

    1. You must be in the directory specific to the level
    """
    create_buildblueprint_backend.run(**kwargs, _is_cli=True)
