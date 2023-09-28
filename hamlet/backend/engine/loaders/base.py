import json
import os
import typing

from hamlet.backend.engine.common import ENGINE_STATE_FILE_NAME
from hamlet.backend.engine.engine import Engine, InstalledEngine
from hamlet.backend.engine.engine_loader import EngineLoader


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
