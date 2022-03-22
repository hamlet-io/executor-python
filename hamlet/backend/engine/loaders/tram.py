import typing
import datetime

from hamlet.backend.engine.engine_loader import EngineLoader

from hamlet.backend.engine.engine import Engine
from hamlet.backend.engine.engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    BashExecutorEnginePart,
    BundledWrapperEnginePart,
)
from hamlet.backend.engine.engine_source import ContainerEngineSource
from hamlet.backend.container_registry import ContainerRepository


class LatestTramEngineLoader(EngineLoader):
    """
    Provides the nightly build of the hamlet base engine image
    This image is tested across all parts and sources as a collection
    Includes testing of system level actions
    """

    def load(self) -> typing.Iterable[Engine]:
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
            BundledWrapperEnginePart(
                source_path="engine-core/image/", source_name="hamlet-engine-base"
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

    def load(self) -> typing.Iterable[Engine]:
        container_repo = ContainerRepository(
            registry_url="https://ghcr.io", repository="hamlet-io/hamlet-engine-base"
        )

        for tag in container_repo.tags:
            if tag.startswith(
                "schedule-"
            ) and datetime.datetime.now() - datetime.datetime.strptime(
                tag.split("-")[1], "%Y%m%d"
            ) <= datetime.timedelta(
                days=90
            ):

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
                    BundledWrapperEnginePart(
                        source_path="engine-core/image/",
                        source_name="hamlet-engine-base",
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
                )
                engine.parts = engine_parts
                engine.sources = engine_sources

                yield engine
