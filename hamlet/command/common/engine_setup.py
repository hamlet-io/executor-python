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
    Always make sure the global engine is installed and that we have at least one engine installed
    """

    engine_store.load_engines(locations=["installed", "global"])

    try:
        engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["installed"])

    except (HamletEngineInvalidVersion, EngineStoreMissingEngineException) as e:
        # If the global engine is old then we need to force it to be the latest
        if isinstance(e, HamletEngineInvalidVersion):
            engine_store.clean_engine(ENGINE_GLOBAL_NAME)

        engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["global"]).install()
        engine_store.load_engines(locations=["installed", "global"], refresh=True)

    # Force an update to the global engine if required
    if (
        engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["installed"]).digest
        != engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["global"]).digest
    ):

        engine_store.get_engines(ENGINE_GLOBAL_NAME, locations=["global"]).install()
        engine_store.load_engines(locations=["installed"], refresh=True)

    if engine_store.global_engine is None:

        default_engine = (
            engine_override if engine_override is not None else ENGINE_DEFAULT_GLOBAL_ENGINE
        )

        try:
            engine_store.get_engine(default_engine, locations=["installed"])

        except EngineStoreMissingEngineException:
            engine_store.load_engines(locations=["local", "remote", "hidden"])
            engine_store.get_engine(
                default_engine, locations=["local", "remote", "hidden"]
            ).install()
            engine_store.load_engines(locations=["installed"], refresh=True)

        engine_store.global_engine = default_engine


def get_engine_env(engine_override):
    """
    Inject the hamlet engine environment variables into the context
    """

    engine_name = engine_override if engine_override else ENGINE_GLOBAL_NAME
    engine = engine_store.get_engine(engine_name, locations=["installed"])
    HAMLET_GLOBAL_CONFIG.engine_environment = engine.environment
