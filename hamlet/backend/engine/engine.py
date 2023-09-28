import hashlib
import json
import os
import platform
import shutil
from abc import ABC, abstractmethod

from hamlet.backend.common.exceptions import BackendException

from .common import ENGINE_STATE_FILE_NAME, ENGINE_STATE_VERSION
from .engine_part import EnginePartInterface
from .engine_source import EngineSourceInterface
from .exceptions import HamletEngineInvalidVersion


class EngineInterface(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self._engine_state_filename = ENGINE_STATE_FILE_NAME

        self._location = None
        self._digest = None

        self._engine_dir = None
        self._engine_state = {
            "name": self.name,
            "description": self.description,
        }

        self._parts = {}
        self._sources = {}

    @property
    def engine_dir(self):
        """
        The engine dir defines the base folder where engines are kept
        """
        return self._engine_dir

    @property
    def location(self):
        """
        The location of engine
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Set the location of this engine ( defined at load time )
        """
        self._location = location

    @engine_dir.setter
    def engine_dir(self, engine_dir):
        """
        The engine dir is set as part of the loader process
        """
        self._engine_dir = engine_dir
        self._load_engine_state()

    @property
    def install_path(self):
        """
        The install path is where the components of the engine will be installed
        """
        return os.path.join(self.engine_dir, self.name)

    @property
    def engine_state_file(self):
        """
        The install state file is a persistant file that holds the install_state
        """
        return os.path.join(self.install_path, self._engine_state_filename)

    @property
    def install_state(self):
        """
        The install state contains the details about the installation
        """
        return None

    def update_install_state(self, source_install_state=None):
        """
        Builds the internal state and saves it to the persistent store
        """
        source_digests = []
        source_install_details = {}
        if source_install_state is not None:
            source_digests = [s.digest for s in source_install_state]
            source_install_details = [vars(s) for s in source_install_state]

        install_state = {
            "part_paths": self._get_part_paths(),
            "digest": self._format_engine_digest(source_digests),
            "source_install_state": source_install_details,
        }

        self._engine_state["version"] = ENGINE_STATE_VERSION
        self._engine_state["install"] = install_state
        self._save_engine_state()

    @property
    def digest(self):
        """
        returns the digest of the engine
        """
        if self._digest is None:
            self._digest = self._format_engine_digest([s.digest for s in self.sources])

        return self._digest

    @property
    def short_digest(self):
        return self.digest[len("sha256:") : 15]

    @property
    def parts(self):
        """
        Parts link concrete hamlet components to sources
        """
        return self._parts.values()

    @parts.setter
    def parts(self, parts):
        for part in parts:
            if isinstance(part, EnginePartInterface):
                self._parts[part.type] = part
            else:
                raise ValueError("part is not an EnginePart")

    @parts.deleter
    def parts(self, type):
        try:
            del self._parts[type]
        except KeyError:
            raise BackendException(f"part {type} not found")

    @property
    def sources(self):
        """
        A source defines an external location which implements engine part(s)
        """
        return self._sources.values()

    @sources.setter
    def sources(self, sources):
        for source in sources:
            if isinstance(source, EngineSourceInterface):
                self._sources[source.name] = source
            else:
                raise ValueError("source is not an EngineSource")

    @sources.deleter
    def sources(self, source_name):
        try:
            del self._sources[source_name]
        except KeyError:
            raise BackendException(f"source {source_name} not found")

    @property
    def part_paths(self):
        """
        Part paths list the physical location of an installed part for a given engine
        """
        if self.install_state is not None:
            return self.install_state.get("part_paths", None)
        else:
            return {}

    @property
    def environment(self):
        """
        Using the part parts generate a dict of hamlet environment variables that are used
        to determine where different engine parts are by the executor
        """
        return {}

    def _get_source(self, source_name):
        """
        Get a particular source
        """
        source = None
        try:
            source = self._sources[source_name]
        except KeyError:
            raise BackendException(f"source {source_name} not found in engine")

        return source

    def _get_engine_source_dir(self, source_name):
        """
        Find the location of a source in an engines installation
        """
        source = self._get_source(source_name)
        return os.path.join(self.install_path, source.name)

    def _get_engine_env_dir(self, source_name):
        """
        Find the directory for the source that will be used in env var paths
        """
        source = self._get_source(source_name)
        if source.env_path is not None:
            return source.env_path
        else:
            return self._get_engine_source_dir(source_name)

    def _load_engine_state(self):
        """
        Load the state of an engine based on its install path
        """
        if os.path.isfile(self.engine_state_file):
            with open(self.engine_state_file, "r") as file:
                self._engine_state = json.load(file)
                engine_version = self._engine_state.get("version", "0.0.0")

                if engine_version != ENGINE_STATE_VERSION:
                    raise HamletEngineInvalidVersion(
                        engine_name=self.name,
                        version=engine_version,
                    )

    def _save_engine_state(self):
        """
        Writes the engine state to disk so that it can be accessed between cli runs
        """
        if not os.path.isdir(self.install_path):
            os.makedirs(self.install_path)

        with open(self.engine_state_file, "w") as file:
            json.dump(self._engine_state, file)

    def _get_part_paths(self):
        part_paths = {}
        for part in self.parts:
            part_paths[part.type] = os.path.join(
                self._get_engine_env_dir(part.source_name), part.source_path
            )
        return part_paths

    def _format_engine_digest(self, source_digests):
        return (
            "sha256:"
            + hashlib.sha256(":".join(source_digests).encode("utf-8")).hexdigest()
        )

    @abstractmethod
    def install(self):
        """
        The install method should loop through all sources and run their pull() method
        Once this has been completed the function should run self.update_install_state()
        This will collect the current state once the install has been completed
        """
        pass

    def set_default_engine(self, engine, engine_store):
        """
        A hook to run when an engine_store is set to a new default
        """
        pass


class InstalledEngine(EngineInterface):
    def __init__(self, name, description, digest, state_version):
        super().__init__(name, description)
        self._installed_digest = digest
        self._engine_state["version"] = state_version

    @property
    def environment(self):
        """
        Using the part parts generate a dict of hamlet environment variables that are used
        to determine where different engine parts are by the executor
        """

        _environment = {
            "GENERATION_ENGINE_DIR": [{"part_type": "core-engine", "env_path": ""}],
            "GENERATION_PLUGIN_DIRS": [
                {"part_type": "engine-plugin-aws", "env_path": ""},
                {"part_type": "engine-plugin-azure", "env_path": ""},
            ],
            "GENERATION_WRAPPER_LOCAL_JAVA": [
                {
                    "env_value": "false"
                    if "bundled-engine-wrapper" in self.part_paths
                    else "true"
                }
            ],
            "GENERATION_WRAPPER_SCRIPT_FILE": [
                {
                    "part_type": "bundled-engine-wrapper",
                    "env_path": f"freemarker-wrapper-{platform.system()}/bin/freemarker-wrapper"
                    if platform.system() != "Windows"
                    else f"freemarker-wrapper-{platform.system()}/bin/freemarker-wrapper.bat",
                }
            ],
            "GENERATION_WRAPPER_JAR_FILE": [
                {"part_type": "engine-wrapper", "env_path": "freemarker-wrapper.jar"}
            ],
            "GENERATION_BASE_DIR": [{"part_type": "executor-bash", "env_path": ""}],
            "GENERATION_DIR": [{"part_type": "executor-bash", "env_path": "cli"}],
            "AUTOMATION_DIR": [
                {"part_type": "executor-bash", "env_path": "automation/jenkins/aws"}
            ],
            "AUTOMATION_BASE_DIR": [
                {"part_type": "executor-bash", "env_path": "automation"}
            ],
        }

        env_result = {}
        self._load_engine_state()
        if self.part_paths is not None:
            for k, part_mappings in _environment.items():
                env_values = []
                for part_mapping in part_mappings:
                    if "env_value" in part_mapping:
                        env_values.append(part_mapping["env_value"])

                    if (
                        "part_type" in part_mapping
                        and self.part_paths.get(part_mapping["part_type"], None)
                        is not None
                    ):
                        env_values.append(
                            os.path.dirname(
                                os.path.join(
                                    self.part_paths[part_mapping["part_type"]],
                                    part_mapping["env_path"],
                                )
                                + "/"
                            )
                        )
                env_result[k] = ";".join(env_values)
        return env_result

    @property
    def digest(self):
        return self._installed_digest

    def install(self):
        self.update_install_state()

    @property
    def install_state(self):
        """
        The install state contains the details about the installation
        """
        self._load_engine_state()
        return self._engine_state.get("install", None)


class Engine(EngineInterface):
    def install(self):
        if os.path.isdir(self.install_path):
            shutil.rmtree(self.install_path)

        source_details = []
        for source in self.sources:
            source_dir = self._get_engine_source_dir(source.name)
            source_details.append(source.pull(source_dir))

        self.update_install_state(source_details)
