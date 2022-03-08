import typing
import os
import json

from hamlet.backend.engine.engine_loader import EngineLoader

from hamlet.backend.engine.engine import Engine, ShimEngine, InstalledEngine
from hamlet.backend.engine.engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    CMDBEnginePluginPart,
    BashExecutorEnginePart,
    WrapperEnginePart,
)
from hamlet.backend.engine.engine_source import ShimPathEngineSource

from hamlet.backend.engine.common import (
    ENGINE_STATE_FILE_NAME,
)


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


class InstalledEngineLoader(EngineLoader):
    """
    Discovers any existing engines under a directory and seeds them as basic
    engine implementations
    """

    def __init__(self, engine_dir):
        super().__init__()
        self.engine_dir = engine_dir

    def load(self) -> typing.Iterable[Engine]:

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
            engine = InstalledEngine(
                name=engine_state["name"],
                description=engine_state["description"],
                digest=engine_state["install"]["digest"],
                state_version=engine_state.get("version", "0.0.0"),
            )
            yield engine
