import typing

from abc import ABC
from .engine import Engine


class EngineLoader(ABC):
    """
    The engine loader locates and seeds the engines available to an engine store
    """

    def __init__(self):
        pass

    def load(self) -> typing.Iterable[Engine]:
        """
        Load should locate and build instances of Engines and yield each engine
        """
        for engine in self._engines:
            yield engine
