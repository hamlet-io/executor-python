import click
from .template import template


@click.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True
    )
)
@click.pass_context
def blueprint(ctx, **kwargs):
    ctx.forward(template, level='blueprint')

blueprint.params = list(filter(lambda p: p.name!='level', template.params))
