import click
from .template import template


@click.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
        max_content_width=240
    )
)
@click.pass_context
def blueprint(ctx, **kwargs):
    """
    Create a blueprint output of the segment

    \b
    NOTES:

    1. You must be in the directory specific to the level
    """
    ctx.forward(template, level='blueprint')


def filter_params(option):
    return option.name in [
        'generation_input_source',
        'generation_framework',
        'generation_provider',
        'generation_testcase',
        'generation_scenarios',
        'deployment_unit'
    ]


blueprint.params = list(filter(filter_params, template.params))
