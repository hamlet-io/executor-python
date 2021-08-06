import os
import shutil
import json
from datetime import datetime

from .common import ENGINE_STORE_DEFAULT_DIR, ENGINE_GLOBAL_NAME
from .exceptions import EngineStoreMissingEngineException

from .loaders.base import GlobalEngineLoader, InstalledEngineLoader
from .loaders.unicycle import UnicycleEngineLoader
from .loaders.tram import LatestTramEngineLoader, TramEngineLoader
from .loaders.train import LatestTrainEngineLoader, TrainEngineLoader
from .loaders.user import UserDefinedEngineLoader


class EngineStore:
    """
    The EngineStore manages the collection of engines that can be used for hamlet
    Loaders are assigned to the engine store which provide engines to the store
    It manages the location of the engine installations and maintains a persistant state
    that tracks global properties that effect all engines
    """

    def __init__(self, store_dir):
        self._engines = {}
        self.store_dir = store_dir
        self._store_state_file = os.path.join(self.store_dir, "store_state.json")
        self.engine_dir = os.path.join(self.store_dir, "engines")

        self.store_state = {}
        self.load_store_state()

        self._global_engine = self.store_state.get("global_engine", None)

        self.local_engine_loaders = [
            InstalledEngineLoader(engine_dir=self.engine_dir),
            UserDefinedEngineLoader(),
            GlobalEngineLoader(),
        ]

        self.external_engine_loaders = [
            UnicycleEngineLoader(),
            LatestTramEngineLoader(),
            TramEngineLoader(),
            LatestTrainEngineLoader(),
            TrainEngineLoader(),
        ]

    @property
    def global_engine(self):
        """
        The global engine defines a special engine that uses other engines to provide parts
        the global provides a consistent location that will link to other engine installations
        """
        return self._global_engine

    @global_engine.setter
    def global_engine(self, name):
        """
        Setting the global engine will locate the provided engine then update
        its symlinks to point to the provided engine.
        """
        global_engine = self.get_engine(ENGINE_GLOBAL_NAME)
        engine = self.get_engine(name)

        for type, path in global_engine.part_paths.items():
            if os.path.islink(path):
                os.unlink(path)

            if os.path.isdir(path):
                os.rmdir(path)

            if engine.part_paths.get(type, None):
                os.symlink(engine.part_paths[type], path, target_is_directory=True)
            else:
                os.makedirs(path)

        self._global_engine = engine.name

        self.store_state = {"global_engine": self.global_engine}
        self.save_store_state()

    def _load_local_engines(self):
        for loader in self.local_engine_loaders:
            for engine in loader.load():
                engine.engine_dir = self.engine_dir
                self._engines[engine.name] = engine

    def _load_external_engines(self, cache_timeout):
        if (
            datetime.now()
            - datetime.strptime(
                self.store_state.get(
                    "last_external_load", datetime.now().isoformat(timespec="seconds")
                ),
                "%Y-%m-%dT%H:%M:%S",
            )
        ).seconds >= cache_timeout:

            for loader in self.external_engine_loaders:
                for engine in loader.load():
                    engine.engine_dir = self.engine_dir
                    self._engines[engine.name] = engine

            self.store_state["last_external_load"] = datetime.now().isoformat(
                timespec="seconds"
            )
            self.save_store_state()

    def get_engines(self):
        """
        Return as list of the engines available locally
        """
        self._load_local_engines()
        return list(self._engines.values())

    def get_engine(self, name, allow_missing=False):
        """
        Return an existing engine
        """
        self._load_local_engines()
        result = self._engines.get(name, None)

        if not allow_missing and not result:
            raise EngineStoreMissingEngineException(
                f"Could not find engine {name} in engine store"
            )

        return result

    def find_engines(self, cache_timeout=0):
        """
        Find engines that can be installed from external sources
        """
        self._load_external_engines(cache_timeout)
        return list(self._engines.values())

    def find_engine(self, name, allow_missing=False, cache_timeout=0):
        """
        Find an external engine
        """
        self._load_external_engines(cache_timeout)
        result = self._engines.get(name, None)

        if not allow_missing and not result:
            raise EngineStoreMissingEngineException(
                f"Could not find engine {name} in engine store"
            )

        return result

    def load_store_state(self):
        """
        Load the persisted enginestore state
        """
        if os.path.isfile(self._store_state_file):
            with open(self._store_state_file, "r") as file:
                self.store_state = json.load(file)

    def save_store_state(self):
        """
        Save the persisted enginestore state
        """
        if self.store_state:
            if not os.path.isdir(self.store_dir):
                os.makedirs(self.store_dir)

            with open(self._store_state_file, "w") as file:
                json.dump(self.store_state, file)

    def clean_engines(self):
        if os.path.isdir(os.path.join(self.engine_dir)):
            shutil.rmtree(self.engine_dir)

    def clean_engine(self, name):
        if os.path.isdir(os.path.join(self.engine_dir, name)):
            shutil.rmtree(os.path.join(self.engine_dir, name))


engine_store = EngineStore(store_dir=ENGINE_STORE_DEFAULT_DIR)
