import tempfile
import os
from unittest import mock

from hamlet.backend.engine import EngineStore
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.engine.engine import Engine
from hamlet.backend.engine.loaders.unicycle import UnicycleEngineLoader
from hamlet.backend.engine.engine_part import CoreEnginePart
from hamlet.backend.engine.engine_source import ShimPathEngineSource


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


def test_global_engine_loading():
    """
    Tests that the basic global engine is loaded and can be found
    """
    with tempfile.TemporaryDirectory() as store_dir:
        engine_store = EngineStore(store_dir=store_dir)

        engine_store.load_engines(locations=["global"])
        assert len(engine_store.get_engines()) == 1
        assert (
            engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["global"]).name
            == ENGINE_GLOBAL_NAME
        )

        engine_store.get_engine(ENGINE_GLOBAL_NAME, locations=["global"]).install()
        engine_store.load_engines(locations=["installed"], refresh=True)

        global_engine = engine_store.get_engine(
            ENGINE_GLOBAL_NAME, locations=["installed"]
        )

        assert os.path.isfile(global_engine.engine_state_file)
        generation_dir_path = os.path.join(
            global_engine.install_path, "shim/executor-bash/cli"
        )
        assert global_engine.environment["GENERATION_DIR"] == generation_dir_path

        automation_dir_path = os.path.join(
            global_engine.install_path, "shim/executor-bash/automation/jenkins/aws"
        )
        assert global_engine.environment["AUTOMATION_DIR"] == automation_dir_path


def test_installed_engine_loading():
    """
    Tests that we can discover engines that have been installed
    and that they can be discovered by the InstalledEngine basic loader
    """
    with tempfile.TemporaryDirectory() as store_dir:
        engine_store = EngineStore(store_dir=store_dir)
        assert len(engine_store.get_engines()) == 0

        """
        Engine is created in a directory which matches the engine_store engine search location
        The engine isn't loaded through an engine loader yet
        """
        manually_installed_engine = Engine(
            name="installed_engine", description="an installed engine"
        )
        manually_installed_engine.engine_dir = engine_store.engine_dir

        manually_installed_engine.sources = [
            ShimPathEngineSource(name="shim_source", description="A basic shim engine")
        ]

        manually_installed_engine.parts = [
            CoreEnginePart(source_name="shim_source", source_path="")
        ]

        manually_installed_engine.install()
        assert os.path.isfile(manually_installed_engine.engine_state_file)

        """
        Use the Installed loader to discover the manually installed engine
        """

        engine_store.load_engines(locations=["installed"])

        discovered_engine = engine_store.get_engine("installed_engine")
        assert discovered_engine.name == "installed_engine"

        generation_engine_path = os.path.join(
            discovered_engine.install_path, "shim_source"
        )
        assert (
            discovered_engine.environment["GENERATION_ENGINE_DIR"]
            == generation_engine_path
        )


@mock_container_registry()
def test_unicycle_engine_loading(container_repository):
    """
    tests that we can run source loading from a container
    """

    with tempfile.TemporaryDirectory() as store_dir:
        engine_store = EngineStore(store_dir=store_dir)

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


@mock.patch("hamlet.backend.engine.loaders.user.HAMLET_GLOBAL_CONFIG")
def test_user_engine_loading(global_config):
    """
    Tests the user engine loading process
    """

    with tempfile.TemporaryDirectory() as test_dir:
        with tempfile.TemporaryDirectory() as store_dir:
            with tempfile.TemporaryDirectory() as cli_config_dir:

                type(global_config).config_dir = mock.PropertyMock(
                    return_value=cli_config_dir
                )

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

                engine_store = EngineStore(store_dir=store_dir)

                engine_store.load_engines(locations=["local"])
                engine_store.get_engine("test", locations=["local"]).install()
                engine_store.load_engines(locations=["installed"])

                assert (
                    engine_store.get_engine("test", locations=["installed"]).name
                    == "test"
                )
