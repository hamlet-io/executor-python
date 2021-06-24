import click

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME, ENGINE_DEFAULT_GLOBAL_ENGINE
from hamlet.env import set_engine_env


def setup_initial_engines(engine_override):
    '''
    Sets up the initial engines for the cli to start working
    '''
    use_global_env = False

    global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
    if not global_engine.installed:
        global_engine.install()

    if engine_override is not None:
        engine = engine_store.get_engine(engine_override)
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


def update_engine(engine_override, auto_install):
    '''
    Automatically update the configured engine
    '''
    engine_name = engine_store.global_engine if engine_override is None else engine_override
    engine = engine_store.get_engine(engine_name)

    if not engine.up_to_date:
        if auto_install:
            click.echo(
                click.style(f'[*] update available for {engine_name} - installing update', fg='yellow')
            )
            engine.install()
        else:
            click.echo(
                click.style(
                    (
                        f'[*] update available for {engine_name}'
                        '- run hamlet engine install-engine {engine_name} to update'
                    ),
                    fg='yellow'
                )
            )
