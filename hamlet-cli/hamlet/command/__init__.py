import click

from hamlet.command.common import decorators
from hamlet.command.common.exceptions import backend_handler
from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME, ENGINE_DEFAULT_GLOBAL_ENGINE
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
    use_global_env = False

    global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
    if not global_engine.installed:
        global_engine.install()

    if opts.engine is not None:
        engine = engine_store.get_engine(opts.engine)
    else:
        engine = engine_store.get_engine(ENGINE_DEFAULT_GLOBAL_ENGINE)
        use_global_env = True

    if not engine.installed:
        click.echo(
            click.style(f'[*] Installing hamlet engine - {engine.name}', fg='yellow'),
            err=True
        )
        engine.install()

    if engine_store.global_engine is None:
        click.echo(
            click.style(f'[*] Global engine not set using the default global engine - {engine.name}', fg='yellow'),
            err=True
        )
        engine_store.global_engine = ENGINE_DEFAULT_GLOBAL_ENGINE

    if use_global_env:
        set_engine_env(global_engine.environment)
    else:
        set_engine_env(engine.environment)
