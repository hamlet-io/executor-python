import os
import tempfile
from unittest import mock

from hamlet.backend.engine import EngineStore
from hamlet.backend.engine.loaders.unicycle import UnicycleEngineLoader


def mock_container_registry():
    def decorator(func):
        @mock.patch("hamlet.backend.engine.engine_source.ContainerRepository")
        def wrapper(container_repository, *args, **kwargs):
            container_repository.return_value.get_tag_digest.return_value = "digest[1]"
            container_repository.return_value.get_tag_manifest.return_value = {
                "schemaVersion": 2,
                "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
                "config": {"digest": "config_digest[1]"},
                "layers": [],
            }
            container_repository.return_value.pull.return_value = "digest[1]"

            return func(container_repository, *args, **kwargs)

        return wrapper

    return decorator


@mock_container_registry()
def test_unicycle_engine_loading(container_repository):
    """
    tests that we can run source loading from a container
    """

    with tempfile.TemporaryDirectory() as store_dir:
        engine_store = EngineStore(store_dir=store_dir, config_search_paths=[store_dir])

        engine_store._engine_locations["remote"]["loaders"] = [UnicycleEngineLoader()]

        engine_store.load_engines(locations=["remote"])
        engine_store.get_engine("unicycle", locations=["remote"]).install()

        engine_store.load_engines(locations=["installed"])
        unicycle_engine = engine_store.get_engine("unicycle", locations=["installed"])

        assert unicycle_engine.name == "unicycle"
        assert (
            unicycle_engine.digest
            == engine_store.get_engine("unicycle", locations=["remote"]).digest
        )


def test_user_engine_loading():
    """
    Tests the user engine loading process
    """

    with tempfile.TemporaryDirectory() as test_dir:
        with tempfile.TemporaryDirectory() as store_dir:
            with tempfile.TemporaryDirectory() as cli_config_dir:
                with open(os.path.join(cli_config_dir, "engine"), "w") as engine_file:
                    engine_file.write(
                        (
                            "[engine:test]\n"
                            "\tdescription = test engine\n"
                            "\tsources = test_dir\n"
                            "\tparts = bash\n"
                            "\n"
                            "[engine_source:test_dir]\n"
                            "\ttype = local_dir\n"
                            f"\tlocal_dir_path = {test_dir}\n"
                            "\n"
                            "[engine_part:bash]\n"
                            "\ttype = executor-bash\n"
                            "\tsource_name = test_dir\n"
                        )
                    )

                engine_store = EngineStore(
                    store_dir=store_dir, config_search_paths=[cli_config_dir]
                )

                engine_store.load_engines(locations=["local"], refresh=True)
                engine_store.get_engines()

                engine_store.get_engine("test", locations=["local"]).install()
                engine_store.load_engines(locations=["installed"], refresh=True)

                assert (
                    engine_store.get_engine("test", locations=["installed"]).name
                    == "test"
                )
