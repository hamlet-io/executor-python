import json
import os
import shutil

from .exceptions import EngineStoreMissingEngineException
from .loaders.base import InstalledEngineLoader
from .loaders.train import LatestTrainEngineLoader, TrainEngineLoader
from .loaders.tram import LatestTramEngineLoader, TramEngineLoader
from .loaders.unicycle import UnicycleEngineLoader
from .loaders.user import UserDefinedEngineLoader


class EngineStore:
    """
    The EngineStore manages the collection of engines that can be used for hamlet
    Loaders are assigned to the engine store which provide engines to the store
    It manages the location of the engine installations and maintains a persistant state
    that tracks global properties that effect all engines
    """

    def __init__(self, store_dir, config_search_paths):
        self._engines = []
        self.store_dir = store_dir
        self._store_state_file = os.path.join(self.store_dir, "store_state.json")
        self.engine_dir = os.path.join(self.store_dir, "engines")
        self.config_search_paths = config_search_paths

        self.store_state = {}
        self.load_store_state()

        self._default_engine = self.store_state.get(
            "default_engine", self.store_state.get("global_engine", None)
        )

        self._engine_locations = {
            "installed": {
                "loaded": False,
                "description": "Engines installed in the local engine store",
                "loaders": [
                    InstalledEngineLoader(engine_dir=self.engine_dir),
                ],
            },
            "local": {
                "loaded": False,
                "description": "Local user defined engines that are available",
                "loaders": [
                    UserDefinedEngineLoader(
                        config_search_paths=self.config_search_paths
                    ),
                ],
            },
            "remote": {
                "loaded": False,
                "description": "Engines available from remote locations",
                "loaders": [
                    UnicycleEngineLoader(),
                    LatestTramEngineLoader(),
                    LatestTrainEngineLoader(),
                    TrainEngineLoader(),
                ],
            },
            "hidden": {
                "loaded": False,
                "description": "Engines which are used internally or for release management",
                "loaders": [
                    TramEngineLoader(),
                ],
            },
        }

    @property
    def engine_locations(self):
        return self._engine_locations

    @property
    def default_engine(self):
        """
        The global engine defines a special engine that uses other engines to provide parts
        the global provides a consistent location that will link to other engine installations
        """
        return self._default_engine

    @default_engine.setter
    def default_engine(self, name):
        """
        Setting the default engine loads the engine and calls the  set_default_engine
        hook on all available engines
        """
        if name is None:
            self._default_engine = None
            self.store_state = {"default_engine": None}

        else:
            self.load_engines("installed")
            engine = self.get_engine(name, ["installed"])

            self.load_engines(["local"])

            for local_engine in self.get_engines("local"):
                local_engine.set_default_engine(engine, self)

            self._default_engine = engine.name
            self.store_state = {"default_engine": engine.name}

        self.save_store_state()

    def get_engines(self, locations=None):
        """
        Get availale engines
        """
        if locations is None:
            locations = self.engine_locations.keys()

        return [engine for engine in self._engines if engine.location in locations]

    def get_engine(self, name, locations=None):
        """
        Find an engine
        """
        if locations is None:
            locations = self.engine_locations.keys()

        try:
            result = [
                engine
                for engine in self.get_engines(locations=locations)
                if engine.name == name
            ][0]
        except IndexError:
            raise EngineStoreMissingEngineException(
                (
                    f"[!] Could not find the requested engine\n"
                    f"[!] - name: {name}\n"
                    f"[!] - locations: {locations}\n"
                    "[!] Run hamlet engine list-engines to find the engine"
                )
            )
        return result

    def load_engines(self, locations=None, refresh=False):
        if locations is None:
            locations = self.engine_locations.keys()

        if refresh:
            self._engines = []

        for location in locations:
            try:
                engine_location = self.engine_locations[location]
            except KeyError:
                continue

            if not engine_location["loaded"] or refresh:
                for loader in engine_location["loaders"]:
                    for engine in loader.load():
                        engine.engine_dir = self.engine_dir
                        engine.location = location
                        self._engines.append(engine)
                engine_location["loaded"] = True
        self.save_store_state()

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
