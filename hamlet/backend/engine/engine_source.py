import hashlib
import json
import os
import pathlib
from abc import ABC, abstractmethod

from hamlet.backend.container_registry import ContainerRepository


class EngineSourceInterface(ABC):
    """
    The engine source implements the retrevel of hamlet component artefacts
    Source classes are based on the process require to retrieve the arefacts
    """

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.env_path = None

    @abstractmethod
    def pull(self, dst_dir):
        """
        Pull the source to a local directory
        Must return a status object describing the source state
        """
        return EngineSourcePullState(
            name=self.name, type=self.__class__.__name__, digest=self.name
        )

    @property
    @abstractmethod
    def digest(self):
        """
        Return a digest of the source to use for verification and version updates
        """
        raise NotImplementedError


class LocalDirectoryEngineSource(EngineSourceInterface):
    """
    An engine source that is available from the local file system
    """

    def __init__(self, name, description, env_path):
        super().__init__(name, description=description)
        self.env_path = env_path

    def pull(self, dst_dir):
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)

        return EngineSourcePullState(
            name=self.name,
            type=self.__class__.__name__,
            digest=hashlib.sha256(bytes(self.env_path, encoding="utf8")).hexdigest(),
            source_metadata={"local_path": self.env_path},
        )

    @property
    def digest(self):
        return hashlib.sha256(bytes(self.env_path, encoding="utf8")).hexdigest()


class ContainerEngineSource(EngineSourceInterface):
    """
    Container based engine source which uses docker registries to pull content
    """

    def __init__(
        self,
        name,
        description,
        registry_url,
        repository,
        tag,
        username=None,
        password=None,
    ):
        super().__init__(name, description)

        self.registry_url = registry_url
        self.repository = repository
        self.tag = tag

        self.username = username
        self.password = password

        self._container_repository = ContainerRepository(
            registry_url=self.registry_url,
            repository=self.repository,
            username=self.username,
            password=self.password,
        )

    def pull(self, dst_dir):
        pull_digest = self._container_repository.pull(self.tag, dst_dir)

        return EngineSourcePullState(
            name=self.name,
            type=self.__class__.__name__,
            digest=pull_digest,
            source_metadata={
                "registry_url": self.registry_url,
                "repository": self.repository,
                "tag": self.tag,
            },
            build_metadata=self._get_build_details(dst_dir),
        )

    @property
    def digest(self):
        return self._container_repository.get_tag_digest(self.tag)

    def _get_build_details(self, dst_dir):
        engine_source = ".hamlet/engine_source.json"
        if dst_dir is not None:
            engine_source_paths = pathlib.Path(dst_dir).glob(f"**/{engine_source}")
            build_sources = {}
            for engine_source_path in engine_source_paths:
                with open(engine_source_path, "r") as file:
                    source_name = str(engine_source_path)[
                        len(dst_dir) : len(str(engine_source_path)) - len(engine_source)
                    ]
                    build_sources[source_name] = json.load(file)

            return build_sources


class EngineSourcePullState(dict):
    """
    Provides details about the source that was pulled
    """

    def __init__(self, name, type, digest, source_metadata=None, build_metadata=None):
        self.name = name
        self.type = type
        self.digest = digest
        self.source_metadata = source_metadata
        self.build_metadata = build_metadata
