import click

from hamlet.command.common import decorators
from hamlet.command.common.exceptions import backend_handler
from hamlet.backend.engine import engine_store
from hamlet.env import set_engine_env

@click.group('root')
@decorators.common_engine_options
@decorators.common_district_options
@decorators.common_cli_config_options
@decorators.common_generation_options
@decorators.common_logging_options
@click.pass_context
@backend_handler()
def root(ctx, opts):
    '''
    hamlet deploy
    '''
    if opts.engine is not None:
        engine = engine_store.get_engine(opts.engine)

        if not engine.installed:
            click.echo(
                click.style(f'[*] Installing hamlet engine - {engine.name}', fg='yellow'),
                err=True
            )
            engine.install()

        if engine_store.global_engine is None:
            click.echo(
                click.style(f'[*] No global engine defined, setting global engine - {engine.name}', fg='yellow'),
                err=True
            )
            engine_store.global_engine = engine.name

        set_engine_env(engine.environment)
