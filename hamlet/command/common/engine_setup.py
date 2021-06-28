import click

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME, ENGINE_DEFAULT_GLOBAL_ENGINE
from hamlet.backend.engine.exceptions import HamletEngineInvalidVersion
from hamlet.env import set_engine_env


def setup_global_engine():
    '''
    Always make sure the global engine is installed
    '''

    try:
        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
    except HamletEngineInvalidVersion:
        '''
        If the global engine is old then we need to force it to be the latest
        '''
        engine_store.clean_engine(ENGINE_GLOBAL_NAME)

        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
        global_engine.install()

        if engine_store.global_engine is not None:
            if engine_store.get_engine(engine_store.global_engine).installed:
                engine_store.global_engine = engine_store.global_engine
            else:
                engine_store.global_engine = None

    if not global_engine.installed:
        global_engine.install()


def get_engine_env(engine_override):

    if engine_override is not None:
        engine = engine_store.get_engine(engine_override)
    else:
        engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)

    set_engine_env(engine.environment)


def setup_initial_engines(engine_override):
    '''
    Sets up the initial engines for the cli to start working
    '''
    if engine_store.global_engine is None:

        if engine_override is not None:
            engine = engine_store.get_engine(engine_override)
        else:
            engine = engine_store.get_engine(ENGINE_DEFAULT_GLOBAL_ENGINE)

        if not engine.installed:
            click.echo(
                click.style(f'[*] No default engine found installing default engine - {engine.name}', fg='yellow'),
                err=True
            )
            engine.install()

        click.echo(
            click.style(f'[*] Setting the global engine to the default engine - {engine.name}', fg='yellow'),
            err=True
        )
        engine_store.global_engine = engine.name


def check_engine_update(engine_override):
    '''
    Check for updates to the current engine
    '''
    try:
        engine_name = engine_store.global_engine if engine_override is None else engine_override
        engine = engine_store.get_engine(engine_name)

        if not engine.up_to_date():
            click.echo(
                click.style(
                    (
                        f'[*] engine update available for {engine_name}\n'
                        f'[*]   - to update run: hamlet engine install-engine {engine_name}'
                    ),
                    fg='yellow'
                )
            )
    except Exception:
        click.echo(
            click.style(
                (
                    f'[!] engine update check failed for {engine_name}\n'
                     '[!]   - run hamlet engine list-engines for more details'
                ),
                fg='red'
            )
        )
