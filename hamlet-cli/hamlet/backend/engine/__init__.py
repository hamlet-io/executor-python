import os
import json

from hamlet.backend.common.exceptions import BackendException

from .common import ENGINE_STORE_DEFAULT_DIR
from .engine_loader import GlobalEngineLoader, InstalledEngineLoader, UnicycleEngineLoader


class EngineStore():
    '''
    The EngineStore manages the collection of engines that can be used for hamlet
    Loaders are assigned to the engine store which provide engines to the store
    It manages the location of the engine installations and maintains a persistant state
    that tracks global properties that effect all engines
    '''
    def __init__(self, store_dir):
        self._engines = {}
        self.store_dir = store_dir
        self._store_state_file = os.path.join(self.store_dir, 'store_state.json')
        self.engine_dir = os.path.join(self.store_dir, 'engines')

        self.store_state = None
        self.load_store_state()

        self._global_engine = self.store_state.get('global_engine', None) if self.store_state is not None else None

        self.engine_loaders = [
            InstalledEngineLoader(engine_dir=self.engine_dir),
            GlobalEngineLoader(),
            UnicycleEngineLoader(),
        ]

    @property
    def engines(self):
        '''
        Return the engines that have been loaded into the store
        '''
        self._load_engines()
        return list(filter(lambda x: not x.hidden, self._engines.values()))

    @property
    def global_engine(self):
        '''
        The global engine defines a special engine that uses other engines to provide parts
        the global provides a consistent location that will link to other engine installations
        '''
        return self._global_engine

    @global_engine.setter
    def global_engine(self, name):
        '''
        Setting the global engine will locate the provided engine then update
        its symlinks to point to the provided engine.
        '''
        global_engine = self.get_engine('_global')
        engine = self.get_engine(name)

        for type, path in global_engine.part_paths.items():
            if os.path.islink(path):
                os.unlink(path)

            if os.path.isdir(path):
                os.rmdir(path)

            if engine.part_paths.get(type, None) is not None:
                os.symlink(engine.part_paths[type], path, target_is_directory=True)
            else:
                os.makedirs(path)

        self._global_engine = engine.name

        self.store_state = {
            'global_engine': self.global_engine
        }
        self.save_store_state()

    def _load_engines(self):
        '''
        Get the engines from the loaders
        '''
        for loader in self.engine_loaders:
            for engine in loader.load():
                engine.engine_dir = self.engine_dir
                self._engines[engine.name] = engine

    def get_engine(self, name, allow_missing=False):
        '''
        returns engines matching the name provided
        '''
        self._load_engines()
        result = self._engines.get(name, None)

        if not allow_missing and result is None:
            raise BackendException(f'Could not find engine {name} in engine store')

        return result

    def load_store_state(self):
        '''
        Load the persisted enginestore state
        '''
        if os.path.isfile(self._store_state_file):
            with open(self._store_state_file, 'r') as file:
                self.store_state = json.load(file)

    def save_store_state(self):
        '''
        Save the persisted enginestore state
        '''
        if self.store_state is not None:
            if not os.path.isdir(self.store_dir):
                os.makedirs(self.store_dir)

            with open(self._store_state_file, 'w') as file:
                json.dump(self.store_state, file)


engine_store = EngineStore(store_dir=ENGINE_STORE_DEFAULT_DIR)
