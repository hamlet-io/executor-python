from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.engine.loaders.unicycle import UnicycleEngineLoader


def run(engine, clear_engine):
    clear_engine()

    engine.engine_store._engine_locations["remote"]["loaders"] = [
        UnicycleEngineLoader()
    ]

    engine.engine_store.load_engines(locations=["installed", "global", "remote"])
    engine.engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["global"]).install()
    engine.engine_store.get_engine("unicycle", locations=["remote"]).install()
    engine.engine_store.load_engines(locations=["installed"], refresh=True)

    engine.engine_store.global_engine = "unicycle"

    assert (
        engine.engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["installed"]).name
        == ENGINE_GLOBAL_NAME
    )
    assert (
        engine.engine_store.get_engine("unicycle", locations=["installed"]).name
        == "unicycle"
    )
    assert engine.engine_store.global_engine == "unicycle"
