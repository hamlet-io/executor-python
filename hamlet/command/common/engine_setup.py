import click

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import (
    ENGINE_GLOBAL_NAME,
    ENGINE_DEFAULT_GLOBAL_ENGINE,
)
from hamlet.backend.engine.exceptions import (
    HamletEngineInvalidVersion,
    EngineStoreMissingEngineException,
)
from hamlet.env import HAMLET_GLOBAL_CONFIG


def setup_global_engine(engine_override):
    """
    Always make sure the global engine is installed
    """

    try:
        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
    except HamletEngineInvalidVersion:
        """
        If the global engine is old then we need to force it to be the latest
        """
        engine_store.clean_engine(ENGINE_GLOBAL_NAME)

        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
        global_engine.install()

    if not global_engine.installed or not global_engine.up_to_date():
        global_engine.install()

    if engine_store.global_engine is not None:
        try:
            engine_store.get_engine(engine_store.global_engine).installed

        except EngineStoreMissingEngineException:

            engine_store.find_engine(engine_store.global_engine).install()
            engine_store.global_engine = engine_store.global_engine

    else:
        if not engine_store.global_engine and engine_override:
            engine_name = engine_override
        else:
            engine_name = ENGINE_DEFAULT_GLOBAL_ENGINE

        try:
            engine_store.get_engine(engine_name).installed

        except EngineStoreMissingEngineException:
            click.secho(f"[*] no default engine set using {engine_name}")
            engine_store.find_engine(engine_name).install()

        engine_store.global_engine = engine_name


def get_engine_env(engine_override):

    if engine_override is not None:
        try:
            engine = engine_store.get_engine(engine_override)

        except EngineStoreMissingEngineException:
            engine = engine_store.find_engine(engine_override, cache_timeout=0)
    else:
        engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)

    HAMLET_GLOBAL_CONFIG.engine_environment = engine.environment


def check_engine_update(engine_override, update_install, cache_timeout=0):
    """
    Check for updates to the current engine
    """
    engine_name = (
        engine_store.global_engine if engine_override is None else engine_override
    )

    try:
        engine = engine_store.find_engine(engine_name, cache_timeout=cache_timeout)

    except EngineStoreMissingEngineException:
        cache_timeout = 0
        engine = engine_store.find_engine(engine_name, cache_timeout=cache_timeout)
        update_install = True

    if not engine.up_to_date(cache_timeout=cache_timeout):

        click.secho("[*] update available for current engine", fg="yellow")

        if update_install:
            click.secho(f"[*] installing {engine_name} update", fg="yellow")

            engine = engine_store.find_engine(engine_name)
            engine.install()
        else:
            click.secho(
                f"[*] to install update run: hamlet engine install-engine {engine_name}",
                fg="yellow",
            )
