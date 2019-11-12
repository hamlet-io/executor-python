import click
from .template import template


@click.command(
    'build-blueprint',
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True
    )
)
@click.pass_context
def build_blueprint(ctx, **kwargs):
    ctx.forward(template, level='buildblueprint')


build_blueprint.params = list(filter(lambda p: p.name != 'level', template.params))
