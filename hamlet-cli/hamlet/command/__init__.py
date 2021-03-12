import click
from hamlet.command.common import decorators


@click.group('root')
@decorators.common_district_options
@decorators.common_cli_config_options
@decorators.common_generation_options
@decorators.common_logging_options
@click.pass_context
def root(ctx, opts):
    '''
    hamlet deploy
    '''
    pass
