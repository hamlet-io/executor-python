import os
import json
import shutil
import hashlib
from abc import ABC, abstractmethod, abstractproperty
from sys import path

from hamlet.backend.common.exceptions import BackendException
from .common import ENGINE_STORE_ENGINES_DIR, ENGINE_STORE_ENGINE_STATE_FILENAME

from .engine_part import EnginePartInterface
from .engine_source import EngineSourceInterface


class EngineInterface(ABC):
    def __init__(self, name, description, hidden=False):
        self.name = name
        self.description = description
        self.hidden = hidden
        self.digest = ''

        self.install_path = os.path.join(ENGINE_STORE_ENGINES_DIR, self.name)
        self.install_state_file = os.path.join(self.install_path, ENGINE_STORE_ENGINE_STATE_FILENAME)

        self.install_state = None
        self.load_install_state()

        self._parts = {}
        self._sources = {}

    _environment = {
        'GENERATION_ENGINE_DIR' : [
            {
                'part_type' :  'core-engine',
                'env_path' : ''
            }
        ],
        'GENERATION_PLUGIN_DIRS' : [
            {
                'part_type' :  'engine-plugin-aws',
                'env_path' : ''
            },
            {
                'part_type' :  'engine-plugin-azure',
                'env_path' : ''
            }
        ],
        'GENERATION_BIN_DIR' : [
            {
                'part_type' :  'engine-binary',
                'env_path' : ''
            }
        ],
        'GENERATION_BASE_DIR'   : [
            {
                'part_type' :  'executor-bash',
                'env_path' : ''
            }
        ],
        'GENERATION_DIR' : [
            {
                'part_type' :  'executor-bash',
                'env_path' : 'cli'
            }
        ],
        'AUTOMATION_DIR' : [
            {
                'part_type' :  'executor-bash',
                'env_path' : 'automation/jenkins/aws'
            }
        ],
        'AUTOMATION_BASE_DIR'  : [
            {
                'part_type' :  'executor-bash',
                'env_path' : 'automation'
            }
        ],
    }

    @property
    def installed(self):
        return True if self.install_state is not None else False

    @property
    def parts(self):
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
        return self.install_state.get('part_paths', None)

    @property
    def environment(self):
        env_result = {}
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
        source = None
        try:
            source = self._sources[source_name]
        except KeyError:
            raise  BackendException(f'source {source_name} not found in engine')

        return source

    def _get_engine_source_dir(self, source_name):
        source = self._get_source(source_name)
        return os.path.join(self.install_path, source.name )

    def load_install_state(self):
        if os.path.isfile(self.install_state_file):
            with open(self.install_state_file, 'r') as file:
                self.install_state = json.load(file)

    def save_install_state(self):
        if not os.path.isdir(self.install_path):
            os.makedirs(self.install_path)

        with open(self.install_state_file, 'w') as file:
            json.dump(self.install_state, file)

    def _set_part_paths(self):
        part_paths = {}
        for part in self.parts:
            part_paths[part.type] = os.path.join(
                self._get_engine_source_dir(part.source_name),
                part.source_path
            )
        return part_paths

    @abstractmethod
    def install(self):
        raise NotImplementedError


class InstalledEngine(EngineInterface):
    def __init__(self, name, description, hidden, digest):
        super().__init__(name, description, hidden=hidden)
        self.digest = digest

    def install():
        pass


class GlobalEngine(EngineInterface):

    def install(self):

        for source in self.sources:
            source_dir = self._get_engine_source_dir(source.name)
            source.pull(source_dir)

        self.install_state = {
            'name' : self.name,
            'description' : self.description,
            'hidden' : self.hidden,
            'digest' : self.digest,
            'part_paths' : self._set_part_paths(),
            'source_digests' : {}
        }
        self.save_install_state()


class Engine(EngineInterface):

    def install(self):

        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path)

        source_digests = {}
        for source in self.sources:
            source_dir = self._get_engine_source_dir(source.name)
            source.pull(source_dir)
            source_digests[source.name] = source.digest

        self.digest = 'sha256:' + hashlib.sha256(':'.join(source_digests.values()).encode('utf-8')).hexdigest()

        self.install_state = {
            'name' : self.name,
            'description' : self.description,
            'hidden' : self.hidden,
            'digest' : self.digest,
            'part_paths' : self._set_part_paths(),
            'source_digests' : source_digests
        }
        self.save_install_state()
