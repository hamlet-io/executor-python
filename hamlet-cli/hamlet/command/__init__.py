import os
import click
from hamlet.command.common.config import Options
from hamlet.command.common.decorators import common_cli_config_options, common_district_options


@click.group('root')
@common_district_options
@common_cli_config_options
@click.pass_context
def root(ctx, opts):
    '''
    hamlet deploy
    '''

    # set global environment variables for template generation
    options = ctx.find_object(Options)
    for k, v in options.to_env_dict().items():
        os.environ[k] = v
