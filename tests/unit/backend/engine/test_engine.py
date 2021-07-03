import tempfile
import os
import hashlib
from unittest import mock

from hamlet.backend.engine import EngineStore
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.engine.engine import Engine
from hamlet.backend.engine.engine_loader import (
    GlobalEngineLoader,
    InstalledEngineLoader,
    UnicycleEngineLoader,
)
from hamlet.backend.engine.engine_part import CoreEnginePart
from hamlet.backend.engine.engine_source import ShimPathEngineSource


def mock_container_registry():
    def decorator(func):
        @mock.patch("hamlet.backend.engine.engine_source.ContainerRepository")
        def wrapper(container_repository, *args, **kwargs):

            container_repository.return_value.get_tag_digest.return_value = (
                "config_digest[1]"
            )
            container_repository.return_value.get_tag_manifest.return_value = {
                "config": {"digest": "config_digest[1]"}
            }
            container_repository.return_value.pull.return_value = {
                "config": {"digest": "config_digest[1]"}
            }

            return func(container_repository, *args, **kwargs)

        return wrapper

    return decorator


def test_global_engine_loading():
    """
    Tests that the basic global engine is loaded and can be found
    """
    with tempfile.TemporaryDirectory() as store_dir:
        engine_store = EngineStore(store_dir=store_dir)

        engine_store.local_engine_loaders = [GlobalEngineLoader()]

        assert len(engine_store.get_engines()) == 1

        global_engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)

        assert global_engine.name == ENGINE_GLOBAL_NAME

        global_engine.install()

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

        engine_store.local_engine_loaders = [
            InstalledEngineLoader(engine_store.engine_dir)
        ]

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

        engine_store.external_engine_loaders = [UnicycleEngineLoader()]

        unicycle_engine = engine_store.find_engine("unicycle")
        unicycle_engine.install()

        assert unicycle_engine.name == "unicycle"

        container_digests = ["config_digest[1]"] * len(unicycle_engine.sources)
        expected_digest = (
            "sha256:"
            + hashlib.sha256(":".join(container_digests).encode("utf-8")).hexdigest()
        )
        assert unicycle_engine.digest == expected_digest
