import typing

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


class UnicycleEngineLoader(EngineLoader):
    """
    Provides the latest builds of all official hamlet components
    Each component is sourced directly from the image that is created on commit to the default branch
    """

    def load(self) -> typing.Iterable[Engine]:
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
