import os
import subprocess
import shutil
import glob
import json

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

    @property
    @abstractmethod
    def build_details(self):
        '''
        Return the details of how the source was built
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def package_details(self):
        '''
        Return the details of how the source was packaged
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

    @property
    def build_details(self):
        return None

    @property
    def package_details(self):
        return None


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

        self._dst_dir = None

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

        self._dst_dir = dst_dir

        auth_token = self._get_auth_token()
        self._manifest = self._get_manifest(auth_token)

        pull_registry_image_to_dir(self.registry_url, self.repository, self._manifest, auth_token, dst_dir)

    @property
    def digest(self):
        if self._manifest is None:
            self._manifest = self._get_manifest()

        return self._manifest['config']['digest']

    @property
    def build_details(self):
        if self._dst_dir is not None:
            engine_source_files = glob.glob(
                os.path.join(self._dst_dir, '**/.hamlet/engine_source.json'),
                recursive=True
            )

            build_sources = {}
            for file in engine_source_files:
                build_sources[file[::len(os.path.commonprefix([self._dst_dir, file]))]] = json.load(file)

            return build_sources

        return None

    @property
    def package_details(self):
        return {
            'provider': 'container',
            'registry_url': self.registry_url,
            'repository': self.repository,
            'tag': self.tag
        }


class EngineSourceBuildData():
    '''
    Provides utility functions that generate version details about
    an engine source as part of its build process
    '''

    def _git_path(self):
        return shutil.which('git')

    def __init__(self, path):
        self.path = path

    def _is_git_repo(self):
        try:
            subprocess.check_output(
                [
                    self._git_path(),
                    'rev-parse',
                    '--is-inside-work-tree',
                ],
                cwd=self.path,
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError:
            return False

        return True

    def _git_current_revision(self):
        return subprocess.check_output(
            [
                self._git_path(),
                'rev-parse',
                'HEAD',
            ],
            cwd=self.path,
            text=True
        ).strip()

    def _git_current_tag(self):
        return subprocess.check_output(
            [
                self._git_path(),
                'tag',
                '--points-at',
                'HEAD',
            ],
            cwd=self.path,
            text=True
        ).strip()

    def _git_current_origin(self):
        return subprocess.check_output(
            [
                self._git_path(),
                'remote',
                'get-url',
                'origin',
            ],
            cwd=self.path,
            text=True
        ).strip()

    @property
    def details(self):

        details = {}

        if self._is_git_repo():
            details['code_source'] = {
                'provider': 'git',
                'revision': self._git_current_revision(),
                'tag': self._git_current_tag(),
                'origin': self._git_current_origin()
            }

        return details
