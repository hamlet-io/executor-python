import click
from .template import template, create_template_backend


@click.command(
    'blueprint',
    short_help='Create a blueprint output of the segment',
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
        max_content_width=240
    )
)
def blueprint(**kwargs):
    """
    Create a blueprint output of the segment

    \b
    NOTES:

    1. You must be in the directory specific to the level
    """
    create_template_backend.run(**kwargs)


def filter_params(option):
    return option.name in [
        'generation_input_source',
        'generation_framework',
        'generation_provider',
        'generation_testcase',
        'generation_scenarios'
    ]


blueprint.params = list(filter(filter_params, template.params))
