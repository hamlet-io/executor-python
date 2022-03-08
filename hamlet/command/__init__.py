import click

from hamlet.command.common import decorators

try:
    from hamlet.__version__ import version
except ImportError:
    version = "unknown"


@click.group("root", context_settings=dict(max_content_width=240))
@click.version_option(version)
@decorators.common_cli_config_options
@decorators.common_generation_options
@decorators.common_logging_options
@decorators.common_engine_options
@decorators.common_district_options
@click.pass_context
def root(ctx, opts):
    """
    hamlet
    """
    pass
