import typing
import re

from hamlet.backend.engine.engine_loader import EngineLoader

from hamlet.backend.engine.engine import Engine
from hamlet.backend.engine.engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    BashExecutorEnginePart,
    WrapperEnginePart,
)
from hamlet.backend.engine.engine_source import ContainerEngineSource
from hamlet.backend.container_registry import ContainerRepository


class LatestTrainEngineLoader(EngineLoader):
    """
    Provides the latest Train release
    """

    def load(self) -> typing.Iterable[Engine]:

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

    def load(self) -> typing.Iterable[Engine]:

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
