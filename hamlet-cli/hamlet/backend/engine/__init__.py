import os
import json

from hamlet.backend.common.exceptions import BackendException

from .common import ENGINE_STORE_DIR
from .engine_loader import GlobalEngineLoader, InstalledEngineLoader, UnicycleEngineLoader


class EngineStore():
    def __init__(self):
        self._engines = {}
        self.store_state_file = os.path.join(ENGINE_STORE_DIR, 'store_state.json')

        self.store_state = None
        self.load_store_state()

        self._global_engine = self.store_state.get('global_engine', None) if self.store_state is not None else None

    engine_loaders = [
        InstalledEngineLoader(),
        GlobalEngineLoader(),
        UnicycleEngineLoader(),
    ]

    @property
    def engines(self):
        self._load_engines()
        return list(filter(lambda x: not x.hidden, self._engines.values()))

    @property
    def global_engine(self):
        return self._global_engine

    @global_engine.setter
    def global_engine(self, name):
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

    def get_engine(self, name, allow_missing=False):
        '''
        returns engines matching the name and version provided
        '''
        self._load_engines()
        result = self._engines.get(name, None)

        if not allow_missing and result is None:
            raise BackendException(f'Could not find engine {name} in engine store')

        return result

    def _load_engines(self):
        '''
        Get the engines from the loaders
        '''
        for loader in self.engine_loaders:
            for engine in loader.engines:
                self._engines[engine.name] = engine

    def load_store_state(self):
        if os.path.isfile(self.store_state_file):
            with open(self.store_state_file, 'r') as file:
                self.store_state = json.load(file)

    def save_store_state(self):
        if self.store_state is not None:
            if not os.path.isdir(ENGINE_STORE_DIR):
                os.makedirs(ENGINE_STORE_DIR)

            with open(self.store_state_file, 'w') as file:
                json.dump(self.store_state, file)


engine_store = EngineStore()
