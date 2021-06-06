import os
import json

from abc import ABC

from .engine import Engine, InstalledEngine, GlobalEngine
from .engine_source import ContainerEngineSource, ShimPathEngineSource
from .engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    CMDBEnginePluginPart,
    BinaryEnginePart,
    BashExecutorEnginePart
)
from .common import (
    ENGINE_GLOBAL_NAME,
    ENGINE_STATE_FILE_NAME
)


class EngineLoader(ABC):
    def __init__(self):
        self._engines = []

    def load(self):
        for engine in self._engines:
            yield engine


class GlobalEngineLoader(EngineLoader):
    '''
    A hidden engine used to provide the path mappings for the shim global engine
    '''
    def __init__(self):
        super().__init__()

        engine_source = [
            ShimPathEngineSource(
                name='shim',
                description='shim based root dir source'
            )
        ]

        engine_parts = [
            CoreEnginePart(
                source_path='engine-core',
                source_name='shim'
            ),
            BashExecutorEnginePart(
                source_path='executor-bash',
                source_name='shim'
            ),
            AWSEnginePluginPart(
                source_path='engine-plugin-aws',
                source_name='shim'
            ),
            AzureEnginePluginPart(
                source_path='engine-plugin-azure',
                source_name='shim'
            ),
            CMDBEnginePluginPart(
                source_path='engine-plugin-cmdb',
                source_name='shim'
            ),
            BinaryEnginePart(
                source_path='engine-binary',
                source_name='shim'
            )
        ]

        engine = GlobalEngine(
            name=ENGINE_GLOBAL_NAME,
            description='The engine used to provide global part mappings',
            hidden=True
        )
        engine.parts = engine_parts
        engine.sources = engine_source

        self._engines = [engine]


class InstalledEngineLoader(EngineLoader):
    '''
    Loads the installed engines to handle failures in loading external engines
    '''

    def __init__(self, engine_dir):
        super().__init__()
        self.engine_dir = engine_dir

    def load(self):

        engine_states = []
        if os.path.isdir(self.engine_dir):
            with os.scandir(self.engine_dir) as engines:
                for engine in engines:
                    if engine.is_dir():
                        with os.scandir(engine) as sources:
                            for source in sources:
                                if source.is_file() and source.name == ENGINE_STATE_FILE_NAME:
                                    with open(source, 'r') as f:
                                        engine_states.append(json.load(f))

        for engine_state in engine_states:
            yield InstalledEngine(
                name=engine_state['name'],
                description=engine_state['description'],
                digest=engine_state['digest'],
                hidden=engine_state['hidden'],
            )


class UnicycleEngineLoader(EngineLoader):
    '''
    Provides the latest builds of all official hamlet components
    Each component is sourced directly from the image that is created on commit to the default branch
    '''

    def __init__(self):
        super().__init__()

        engine_sources = [
            ContainerEngineSource(
                name='engine',
                description='hamlet core engine',
                registry_url='https://ghcr.io',
                repository='hamlet-io/engine',
                tag='latest'
            ),
            ContainerEngineSource(
                name='executor-bash',
                description='hamlet bash executor',
                registry_url='https://ghcr.io',
                repository='hamlet-io/executor-bash',
                tag='latest'
            ),
            ContainerEngineSource(
                name='engine-plugin-aws',
                description='hamlet aws engine plugin',
                registry_url='https://ghcr.io',
                repository='hamlet-io/engine-plugin-aws',
                tag='latest'
            ),
            ContainerEngineSource(
                name='engine-plugin-azure',
                description='hamlet azure engine plugin',
                registry_url='https://ghcr.io',
                repository='hamlet-io/engine-plugin-azure',
                tag='latest'
            ),
        ]

        engine_parts = [
            CoreEnginePart(
                source_path='',
                source_name='engine'
            ),
            BashExecutorEnginePart(
                source_path='',
                source_name='executor-bash'
            ),
            AWSEnginePluginPart(
                source_path='',
                source_name='engine-plugin-aws'
            ),
            AzureEnginePluginPart(
                source_path='',
                source_name='engine-plugin-azure'
            ),
        ]

        engine = Engine(
            name='unicycle',
            description='Latest build of the official components'
        )
        engine.parts = engine_parts
        engine.sources = engine_sources

        self._engines = [engine]
