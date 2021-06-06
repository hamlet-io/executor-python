import os
import json
import shutil
import hashlib
from abc import ABC, abstractmethod

from hamlet.backend.common.exceptions import BackendException

from .engine_part import EnginePartInterface
from .engine_source import EngineSourceInterface
from .common import ENGINE_STATE_FILE_NAME


class EngineInterface(ABC):
    def __init__(self, name, description, hidden=False):
        self.name = name
        self.description = description
        self.hidden = hidden

        self.engine_state_filename = ENGINE_STATE_FILE_NAME

        self._engine_dir = None
        self._install_state = {
            'name': self.name,
            'description': self.description,
            'hidden': self.hidden
        }

        self._parts = {}
        self._sources = {}

    _environment = {
        'GENERATION_ENGINE_DIR': [
            {
                'part_type': 'core-engine',
                'env_path': ''
            }
        ],
        'GENERATION_PLUGIN_DIRS': [
            {
                'part_type': 'engine-plugin-aws',
                'env_path': ''
            },
            {
                'part_type': 'engine-plugin-azure',
                'env_path': ''
            }
        ],
        'GENERATION_BIN_DIR': [
            {
                'part_type': 'engine-binary',
                'env_path': ''
            }
        ],
        'GENERATION_BASE_DIR': [
            {
                'part_type': 'executor-bash',
                'env_path': ''
            }
        ],
        'GENERATION_DIR': [
            {
                'part_type': 'executor-bash',
                'env_path': 'cli'
            }
        ],
        'AUTOMATION_DIR': [
            {
                'part_type': 'executor-bash',
                'env_path': 'automation/jenkins/aws'
            }
        ],
        'AUTOMATION_BASE_DIR': [
            {
                'part_type': 'executor-bash',
                'env_path': 'automation'
            }
        ],
    }

    @property
    def installed(self):
        '''
        Check to see if the engine has been installed locally
        '''
        return True if self.digest is not None else False

    @property
    def engine_dir(self):
        '''
        The engine dir defines the base folder where engines are kept
        '''
        return self._engine_dir

    @engine_dir.setter
    def engine_dir(self, engine_dir):
        '''
        The engine dir is set as part of the loader process
        '''
        self._engine_dir = engine_dir
        self._load_install_state()

    @property
    def install_path(self):
        '''
        The install path is where the components of the engine will be installed
        '''
        return os.path.join(self.engine_dir, self.name)

    @property
    def install_state_file(self):
        '''
        The install state file is a persistant file that holds the install_state
        '''
        return os.path.join(self.install_path, self.engine_state_filename)

    @property
    def install_state(self):
        '''
        The install state contains the details about the instaltion
        '''
        self._load_install_state()
        return self._install_state

    def update_install_state(self):
        '''
        Builds the internal state and saves it to the persistant store
        '''
        self._install_state['part_paths'] = self._get_part_paths()
        self._install_state['source_digests'] = self._get_source_digests()
        self._install_state['digest'] = self._format_engine_digest(self._install_state['source_digests'].values())
        self._save_install_state()

    @property
    def digest(self):
        '''
        returns the digests of the current installed sources
        '''
        return self.install_state.get('digest', None)

    @property
    def parts(self):
        '''
        Parts link concrete hamlet components to sources
        '''
        return self._parts.values()

    @parts.setter
    def parts(self, parts):
        for part in parts:
            if isinstance(part, EnginePartInterface):
                self._parts[part.type] = part
            else:
                raise ValueError('part is not an EnginePart')

    @parts.deleter
    def parts(self, type):
        try:
            del self._parts[type]
        except KeyError:
            raise BackendException(f'part {type} not found')

    @property
    def sources(self):
        '''
        A source defines an external location which implements engine part(s)
        '''
        return self._sources.values()

    @sources.setter
    def sources(self, sources):
        for source in sources:
            if isinstance(source, EngineSourceInterface):
                self._sources[source.name] = source
            else:
                raise ValueError('source is not an EngineSource')

    @sources.deleter
    def sources(self, source_name):
        try:
            del self._sources[source_name]
        except KeyError:
            raise BackendException(f'source {source_name} not found')

    @property
    def part_paths(self):
        '''
        Part paths list the physical location of an installed part for a given engine
        '''
        return self.install_state.get('part_paths', None)

    @property
    def environment(self):
        '''
        Using the part parts generate a dict of hamlet environment variables that are used
        to determine where different engine parts are by the executor
        '''
        env_result = {}
        self._load_install_state()
        if self.part_paths is not None:
            for k, part_mappings in self._environment.items():
                env_values = []
                for part_mapping in part_mappings:
                    if self.part_paths.get(part_mapping['part_type'], None) is not None:
                        env_values.append(
                            os.path.dirname(
                                os.path.join(
                                    self.part_paths[part_mapping['part_type']],
                                    part_mapping["env_path"]
                                ) + '/'
                            )
                        )
                env_result[k] = ';'.join(env_values)
        return env_result

    def _get_source(self, source_name):
        '''
        Get a particular source
        '''
        source = None
        try:
            source = self._sources[source_name]
        except KeyError:
            raise BackendException(f'source {source_name} not found in engine')

        return source

    def _get_engine_source_dir(self, source_name):
        '''
        Find the location of a source for within an instllation
        '''
        source = self._get_source(source_name)
        return os.path.join(self.install_path, source.name)

    def _load_install_state(self):
        '''
        Load the state of an engine based on its install path
        '''
        if os.path.isfile(self.install_state_file):
            with open(self.install_state_file, 'r') as file:
                self._install_state = json.load(file)

    def _save_install_state(self):
        '''
        Writes the installation state to disk so that it can be accessed between cli runs
        '''
        if not os.path.isdir(self.install_path):
            os.makedirs(self.install_path)

        with open(self.install_state_file, 'w') as file:
            json.dump(self._install_state, file)

    def _get_part_paths(self):
        part_paths = {}
        for part in self.parts:
            part_paths[part.type] = os.path.join(
                self._get_engine_source_dir(part.source_name),
                part.source_path
            )
        return part_paths

    def _get_source_digests(self):
        '''
        Each source creates a digest that we use to determine updates
        of the overall engine
        '''
        source_digests = {}
        for source in self.sources:
            source_digests[source.name] = source.digest

        return source_digests

    def _format_engine_digest(self, source_digests):
        return 'sha256:' + hashlib.sha256(':'.join(source_digests).encode('utf-8')).hexdigest()

    @abstractmethod
    def install(self):
        '''
        The install method should loop through all sources and run their pull() method
        Once this has been completed the function should run self.update_install_state()
        This will collect the current state once the install has been completed
        '''
        pass


class InstalledEngine(EngineInterface):
    def __init__(self, name, description, digest, hidden):
        super().__init__(name, description, hidden=hidden)
        self._installed_digest = digest

    def digest(self):
        return self._installed_digest

    def install(self):
        self.update_install_state()


class GlobalEngine(EngineInterface):

    def install(self):

        for source in self.sources:
            source_dir = self._get_engine_source_dir(source.name)
            source.pull(source_dir)
        self.update_install_state()


class Engine(EngineInterface):

    def install(self):

        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path)

        for source in self.sources:
            source_dir = self._get_engine_source_dir(source.name)
            source.pull(source_dir)

        self.update_install_state()
