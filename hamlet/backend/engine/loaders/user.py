import click
import typing
import os

from click_configfile import ConfigFileReader, SectionSchema, matches_section
from hamlet.env import HAMLET_GLOBAL_CONFIG

from hamlet.utils import ConfigParam

from hamlet.backend.engine.engine_loader import EngineLoader

from hamlet.backend.engine.engine import Engine
from hamlet.backend.engine.engine_source import (
    LocalDirectoryEngineSource,
    ContainerEngineSource,
)
from hamlet.backend.engine.engine_part import (
    CoreEnginePart,
    AWSEnginePluginPart,
    AzureEnginePluginPart,
    CMDBEnginePluginPart,
    BashExecutorEnginePart,
    WrapperEnginePart,
)


def get_engine_config_dir():
    print("getting engine config")
    return HAMLET_GLOBAL_CONFIG.config_dir


class EngineSchema(object):
    """Defines the schema for engines loaded through a toml based config file"""

    @matches_section("engine:*")
    class Engine(SectionSchema):
        """The engine is the collection of sources and parts that provide an overall hamlet install"""

        #: A general description of the engine
        description = ConfigParam(type=str)

        #: A list of source names defined in engine_source: sections
        sources = ConfigParam(type=str, multiple=True)

        #: A list of part names defined in engine_part: sections
        parts = ConfigParam(type=str, multiple=True)

    @matches_section("engine_source:*")
    class EngineSource(SectionSchema):
        """Engine source configuration"""

        #: A general description of the engine_source
        description = ConfigParam(type=str)

        #: The type of engine_source defines where to get the source from
        type = ConfigParam(type=click.Choice(["local_dir", "container"]))

        #: local_dir type: the local path to the source
        local_dir_path = ConfigParam(
            type=click.Path(dir_okay=True, file_okay=False, readable=True)
        )

        #: container type: the base url for the container registry
        container_registry_url = ConfigParam(type=str)

        #: container type: the name of the container repository
        container_repository = ConfigParam(type=str)

        #: container type: the tag of the image to pull from the repository
        container_tag = ConfigParam(type=str)

    @matches_section("engine_part:*")
    class EnginePart(SectionSchema):
        """Engine part configuration"""

        #: The type of the engine_part defines what function a particular part of the source does in hamlet
        type = ConfigParam(
            type=click.Choice(
                [
                    "engine",
                    "engine-plugin-aws",
                    "engine-plugin-azure",
                    "engine-plugin-cmdb",
                    "executor-bash",
                    "wrapper",
                ]
            )
        )

        #: The name of the source in engine_source: sections that the part belongs to
        source_name = ConfigParam(type=str)

        #: The source_path is the path within the source where the part functions are located
        source_path = ConfigParam(type=str)


class EngineReader(ConfigFileReader):

    """Reader for local engine configuration."""

    config_files = ["engine.ini", "engine"]
    config_name = "engine"
    config_searchpath = []
    config_section_schemas = [
        EngineSchema.Engine,
        EngineSchema.EnginePart,
        EngineSchema.EngineSource,
    ]

    @classmethod
    def select_config_schema_for(cls, section_name):
        section_schema = super(EngineReader, cls).select_config_schema_for(section_name)
        for v in section_schema.__dict__:
            if isinstance(v, ConfigParam):
                v.ctx = cls
        return section_schema

    @classmethod
    def load_engines(cls):
        """Load engines found in the config file."""

        if os.path.exists(HAMLET_GLOBAL_CONFIG.config_dir):
            if os.path.isdir(HAMLET_GLOBAL_CONFIG.config_dir):
                cls.config_searchpath.insert(0, HAMLET_GLOBAL_CONFIG.config_dir)

        config = cls.read_config()

        for k, v in config.items():
            if k.startswith("engine:"):
                engine = Engine(
                    name=k[len("engine:") :],
                    description=v.get("description", None),
                )

                sources = []
                for source_name in v.get("sources"):
                    try:
                        source_config = config[f"engine_source:{source_name}"]

                    except KeyError as e:
                        e.msg = (
                            f"The provided engine source {source_name}"
                            "could not be found in the configured local sources"
                        )
                        raise e

                    if source_config["type"] == "local_dir":
                        sources.append(
                            LocalDirectoryEngineSource(
                                name=source_name,
                                description=source_config.get("description", None),
                                env_path=source_config["local_dir_path"],
                            )
                        )

                    if source_config["type"] == "container":
                        sources.append(
                            ContainerEngineSource(
                                name=source_name,
                                description=source_config.get("description", None),
                                registry_url=source_config.get(
                                    "container_registry_url"
                                ),
                                repository=source_config.get("container_repository"),
                                tag=source_config.get("container_tag"),
                            )
                        )

                parts = []
                for part_name in v.get("parts"):

                    part_config = config[f"engine_part:{part_name}"]

                    part_source_config = {
                        "source_name": part_config["source_name"],
                        "source_path": part_config.get("source_path", ""),
                    }

                    if part_config["type"] == "engine":
                        parts.append(CoreEnginePart(**part_source_config))

                    if part_config["type"] == "engine-plugin-aws":
                        parts.append(AWSEnginePluginPart(**part_source_config))

                    if part_config["type"] == "engine-plugin-azure":
                        parts.append(AzureEnginePluginPart(**part_source_config))

                    if part_config["type"] == "engine-plugin-cmdb":
                        parts.append(CMDBEnginePluginPart(**part_source_config))

                    if part_config["type"] == "executor-bash":
                        parts.append(BashExecutorEnginePart(**part_source_config))

                    if part_config["type"] == "wrapper":
                        parts.append(WrapperEnginePart(**part_source_config))

                engine.sources = sources
                engine.parts = parts

                yield engine


class UserDefinedEngineLoader(EngineLoader):
    """
    Loads a user defined configuration file defining engines and their configuration
    """

    def __init__(self):
        super().__init__()

    def load(self) -> typing.Iterable[Engine]:

        engine_cls = EngineReader
        for engine in engine_cls.load_engines():
            yield engine
