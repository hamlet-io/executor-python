import typing

from hamlet.backend.engine.engine_loader import EngineLoader

from hamlet.backend.engine.engine import Engine, ShimEngine
from hamlet.backend.engine.engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    CMDBEnginePluginPart,
    BashExecutorEnginePart,
    WrapperEnginePart,
    BundledWrapperEnginePart,
)
from hamlet.backend.engine.engine_source import ShimPathEngineSource


class ShimEngineLoader(EngineLoader):
    """
    Seeds an engine used to create a known engine directory that can be used to establish
    a standard location for hamlet scripts called outside of the cli
    """

    def load(self) -> typing.Iterable[Engine]:
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

        engine = ShimEngine(
            name="shim",
            description="The engine used to provide shim based access to a fixed diretory",
        )
        engine.parts = engine_parts
        engine.sources = engine_source

        yield engine


class BundledShimEngineLoader(EngineLoader):
    """
    Seeds an engine used to create a known engine directory that can be used to establish
    a standard location for hamlet scripts called outside of the cli
    """

    def load(self) -> typing.Iterable[Engine]:
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
            BundledWrapperEnginePart(source_path="engine-wrapper", source_name="shim"),
        ]

        engine = ShimEngine(
            name="bundled_shim",
            description="The engine used to provide shim based access to a fixed diretory",
        )
        engine.parts = engine_parts
        engine.sources = engine_source

        yield engine
