from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME


def run(engine, clear_engine):
    clear_engine()

    global_engine = engine.engine_store.get_engine(ENGINE_GLOBAL_NAME)
    global_engine.install()

    unicycle_engine = engine.engine_store.find_engine("unicycle")
    unicycle_engine.install()

    engine.engine_store.global_engine = "unicycle"

    assert global_engine.installed is True
    assert unicycle_engine.installed is True

    assert engine.engine_store.global_engine == "unicycle"
