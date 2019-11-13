import click
from .template import template


@click.command(
    'build-blueprint',
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
        max_content_width=240
    )
)
@click.pass_context
def build_blueprint(ctx, **kwargs):
    """
    Create a blueprint output for the provided deployment unit

    \b
    NOTES:

    1. You must be in the directory specific to the level
    """
    ctx.forward(template, level='buildblueprint')


def filter_params(option):
    return option.name in [
        'generation_input_source',
        'generation_framework',
        'generation_scenarios',
        'generation_testcase',
        'deployment_unit'
    ]


build_blueprint.params = list(filter(filter_params, template.params))
