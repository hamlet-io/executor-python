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

    try:
        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
    except HamletEngineInvalidVersion:

        # If the global engine is old then we need to force it to be the latest
        engine_store.clean_engine(ENGINE_GLOBAL_NAME)

        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
        global_engine.install()

    if not global_engine.installed or not global_engine.up_to_date():
        global_engine.install()

    if engine_store.global_engine is None:

        if engine_override:
            default_engine = engine_override
        else:
            default_engine = ENGINE_DEFAULT_GLOBAL_ENGINE

        try:
            engine_store.get_engine(default_engine)

        except EngineStoreMissingEngineException:
            engine_store.find_engine(default_engine).install()

        engine_store.global_engine = default_engine


def get_engine_env(engine_override):
    """
    Inject the hamlet engine environment variables into the context
    """

    if engine_override is not None:
        engine = engine_store.get_engine(engine_override)
    else:
        engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)

    HAMLET_GLOBAL_CONFIG.engine_environment = engine.environment
