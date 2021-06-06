import os
from abc import ABC, abstractmethod

from hamlet.backend.container_registry import (
    get_registry_login_token,
    get_registry_image_manifest,
    pull_registry_image_to_dir
)


class EngineSourceInterface(ABC):
    '''
    The engine source implements the retrevel of hamlet component artefacts
    Source classes are based on the process require to retrieve the arefacts
    '''

    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    @abstractmethod
    def pull(self, dst_dir):
        '''
        Pull the source to a local directory
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def digest(self):
        '''
        Return a digest of the source to use for verification and version updates
        '''
        raise NotImplementedError


class ShimPathEngineSource(EngineSourceInterface):
    '''
    Sets a standard source path to use for shim based providers
    '''

    def pull(self, dst_dir):
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)

    @property
    def digest(self):
        return self.name


class ContainerEngineSource(EngineSourceInterface):
    '''
    Container based engine source which uses docker registries to pull content
    '''

    def __init__(self, name, description, registry_url, repository, tag, username=None, password=None):
        super().__init__(name, description)

        self.registry_url = registry_url
        self.repository = repository
        self.tag = tag

        self.username = username
        self.password = password

        self._manifest = None

    def _get_auth_token(self):
        return get_registry_login_token(
            self.registry_url,
            self.repository,
            username=self.username,
            password=self.password
        )

    def _get_manifest(self, auth_token=None):
        if auth_token is None:
            auth_token = self._get_auth_token()
        if self._manifest is None:
            return get_registry_image_manifest(self.registry_url, self.repository, self.tag, auth_token)
        else:
            return self._manifest

    def pull(self, dst_dir):

        auth_token = self._get_auth_token()
        self._manifest = self._get_manifest(auth_token)

        pull_registry_image_to_dir(self.registry_url, self.repository, self._manifest, auth_token, dst_dir)

    @property
    def digest(self):
        if self._manifest is None:
            self._manifest = self._get_manifest()

        return self._manifest['config']['digest']
