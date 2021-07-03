import os
import json
import re

from abc import ABC

from .engine import Engine, InstalledEngine, GlobalEngine
from .engine_source import ContainerEngineSource, ShimPathEngineSource
from .engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    CMDBEnginePluginPart,
    BashExecutorEnginePart,
    WrapperEnginePart,
)
from .common import (
    ENGINE_GLOBAL_NAME,
    ENGINE_STATE_FILE_NAME,
)
from hamlet.backend.container_registry import ContainerRepository


class EngineLoader(ABC):
    def __init__(self):
        pass

    def load(self, local_only):
        for engine in self._engines:
            yield engine


class GlobalEngineLoader(EngineLoader):
    """
    A hidden engine used to provide the path mappings for the shim global engine
    """

    def load(self):
        engine_source = [
            ShimPathEngineSource(name="shim", description="shim based root dir source")
        ]

        engine_parts = [
            CoreEnginePart(source_path="engine-core", source_name="shim"),
            BashExecutorEnginePart(source_path="executor-bash", source_name="shim"),
            AWSEnginePluginPart(source_path="engine-plugin-aws", source_name="shim"),
            AzureEnginePluginPart(
                source_path="engine-plugin-azure", source_name="shim"
            ),
            CMDBEnginePluginPart(source_path="engine-plugin-cmdb", source_name="shim"),
            WrapperEnginePart(source_path="engine-wrapper", source_name="shim"),
        ]

        engine = GlobalEngine(
            name=ENGINE_GLOBAL_NAME,
            description="The engine used to provide global part mappings",
            hidden=True,
        )
        engine.parts = engine_parts
        engine.sources = engine_source

        yield engine


class InstalledEngineLoader(EngineLoader):
    """
    Loads the installed engines to handle failures in loading external engines
    """

    def __init__(self, engine_dir):
        super().__init__()
        self.engine_dir = engine_dir

    def load(self):

        engine_states = []
        if os.path.isdir(self.engine_dir):
            with os.scandir(self.engine_dir) as engines:
                for engine in engines:
                    if engine.is_dir():
                        with os.scandir(engine) as sources:
                            for source in sources:
                                if (
                                    source.is_file()
                                    and source.name == ENGINE_STATE_FILE_NAME
                                ):
                                    with open(source, "r") as f:
                                        engine_states.append(json.load(f))

        for engine_state in engine_states:
            yield InstalledEngine(
                name=engine_state["name"],
                description=engine_state["description"],
                digest=engine_state["install"]["digest"],
                hidden=engine_state["hidden"],
                state_version=engine_state.get("version", "0.0.0"),
            )


class UnicycleEngineLoader(EngineLoader):
    """
    Provides the latest builds of all official hamlet components
    Each component is sourced directly from the image that is created on commit to the default branch
    """

    def load(self):
        engine_sources = [
            ContainerEngineSource(
                name="engine",
                description="hamlet core engine",
                registry_url="https://ghcr.io",
                repository="hamlet-io/engine",
                tag="edge",
            ),
            ContainerEngineSource(
                name="executor-bash",
                description="hamlet bash executor",
                registry_url="https://ghcr.io",
                repository="hamlet-io/executor-bash",
                tag="edge",
            ),
            ContainerEngineSource(
                name="engine-plugin-aws",
                description="hamlet aws engine plugin",
                registry_url="https://ghcr.io",
                repository="hamlet-io/engine-plugin-aws",
                tag="edge",
            ),
            ContainerEngineSource(
                name="engine-plugin-azure",
                description="hamlet azure engine plugin",
                registry_url="https://ghcr.io",
                repository="hamlet-io/engine-plugin-azure",
                tag="edge",
            ),
            ContainerEngineSource(
                name="engine-core",
                description="hamlet freemarker wrapper",
                registry_url="https://ghcr.io",
                repository="hamlet-io/engine-core",
                tag="edge",
            ),
        ]

        engine_parts = [
            WrapperEnginePart(source_path="", source_name="engine-core"),
            CoreEnginePart(source_path="", source_name="engine"),
            BashExecutorEnginePart(source_path="", source_name="executor-bash"),
            AWSEnginePluginPart(source_path="", source_name="engine-plugin-aws"),
            AzureEnginePluginPart(source_path="", source_name="engine-plugin-azure"),
        ]

        engine = Engine(
            name="unicycle", description="Latest build of the official engine parts"
        )
        engine.parts = engine_parts
        engine.sources = engine_sources

        yield engine


class LatestTramEngineLoader(EngineLoader):
    """
    Provides the nightly build of the hamlet base engine image
    This image is tested across all parts and sources as a collection
    Includes testing of system level actions
    """

    def load(self):
        engine_sources = [
            ContainerEngineSource(
                name="hamlet-engine-base",
                description="hamlet official engine source",
                registry_url="https://ghcr.io",
                repository="hamlet-io/hamlet-engine-base",
                tag="nightly",
            ),
        ]

        engine_parts = [
            WrapperEnginePart(
                source_path="engine-core/", source_name="hamlet-engine-base"
            ),
            CoreEnginePart(source_path="engine/", source_name="hamlet-engine-base"),
            BashExecutorEnginePart(
                source_path="executor-bash/", source_name="hamlet-engine-base"
            ),
            AWSEnginePluginPart(
                source_path="engine-plugin-aws/", source_name="hamlet-engine-base"
            ),
            AzureEnginePluginPart(
                source_path="engine-plugin-azure/", source_name="hamlet-engine-base"
            ),
        ]

        engine = Engine(name="tram", description="Nightly build of the official engine")
        engine.parts = engine_parts
        engine.sources = engine_sources

        yield engine


class TramEngineLoader(EngineLoader):
    """
    Provides all of the tram releases which have been created
    """

    def load(self):
        container_repo = ContainerRepository(
            registry_url="https://ghcr.io", repository="hamlet-io/hamlet-engine-base"
        )

        for tag in container_repo.tags:
            if tag.startswith("schedule-"):

                engine_sources = [
                    ContainerEngineSource(
                        name="hamlet-engine-base",
                        description="hamlet official engine source",
                        registry_url="https://ghcr.io",
                        repository="hamlet-io/hamlet-engine-base",
                        tag=tag,
                    ),
                ]

                engine_parts = [
                    WrapperEnginePart(
                        source_path="engine-core/", source_name="hamlet-engine-base"
                    ),
                    CoreEnginePart(
                        source_path="engine/", source_name="hamlet-engine-base"
                    ),
                    BashExecutorEnginePart(
                        source_path="executor-bash/", source_name="hamlet-engine-base"
                    ),
                    AWSEnginePluginPart(
                        source_path="engine-plugin-aws/",
                        source_name="hamlet-engine-base",
                    ),
                    AzureEnginePluginPart(
                        source_path="engine-plugin-azure/",
                        source_name="hamlet-engine-base",
                    ),
                ]

                engine = Engine(
                    name=tag.replace("schedule-", "tram-"),
                    description="Scheduled build of the official hamlet engine",
                    hidden=True,
                )
                engine.parts = engine_parts
                engine.sources = engine_sources

                yield engine


class LatestTrainEngineLoader(EngineLoader):
    """
    Provides the latest Train release
    """

    def load(self):

        engine_sources = [
            ContainerEngineSource(
                name="hamlet-engine-base",
                description="hamlet official engine source",
                registry_url="https://ghcr.io",
                repository="hamlet-io/hamlet-engine-base",
                tag="latest",
            ),
        ]

        engine_parts = [
            WrapperEnginePart(
                source_path="engine-core/", source_name="hamlet-engine-base"
            ),
            CoreEnginePart(source_path="engine/", source_name="hamlet-engine-base"),
            BashExecutorEnginePart(
                source_path="executor-bash/", source_name="hamlet-engine-base"
            ),
            AWSEnginePluginPart(
                source_path="engine-plugin-aws/", source_name="hamlet-engine-base"
            ),
            AzureEnginePluginPart(
                source_path="engine-plugin-azure/", source_name="hamlet-engine-base"
            ),
        ]

        engine = Engine(
            name="train", description="The latest release of the official hamlet engine"
        )
        engine.parts = engine_parts
        engine.sources = engine_sources

        self._engines = [engine]

        yield engine


class TrainEngineLoader(EngineLoader):
    """
    Provides all of the tram releases which have been created
    These are considered the Train Release Candidates and can be used for managing releases
    """

    def load(self):

        container_repo = ContainerRepository(
            registry_url="https://ghcr.io", repository="hamlet-io/hamlet-engine-base"
        )

        for tag in container_repo.tags:
            if re.fullmatch("^v?[0-9]*.[0-9]*.[0-9]*.$", tag) is not None:

                engine_sources = [
                    ContainerEngineSource(
                        name="hamlet-engine-base",
                        description="hamlet official engine source",
                        registry_url="https://ghcr.io",
                        repository="hamlet-io/hamlet-engine-base",
                        tag=tag,
                    ),
                ]

                engine_parts = [
                    WrapperEnginePart(
                        source_path="engine-core/", source_name="hamlet-engine-base"
                    ),
                    CoreEnginePart(
                        source_path="engine/", source_name="hamlet-engine-base"
                    ),
                    BashExecutorEnginePart(
                        source_path="executor-bash/", source_name="hamlet-engine-base"
                    ),
                    AWSEnginePluginPart(
                        source_path="engine-plugin-aws/",
                        source_name="hamlet-engine-base",
                    ),
                    AzureEnginePluginPart(
                        source_path="engine-plugin-azure/",
                        source_name="hamlet-engine-base",
                    ),
                ]

                engine = Engine(
                    name=tag,
                    description="Stable release of the official hamlet engine",
                )
                engine.parts = engine_parts
                engine.sources = engine_sources

                yield engine
