from abc import ABC


class EnginePartInterface(ABC):
    """
    An engine part defines a functional component of the hamlet tooling
    Each part has a fixed type with instances have a link to a source that
    has the component tooling
    """

    type = None
    description = ""

    def __init__(self, source_name, source_path):
        self.source_path = source_path
        self.source_name = source_name


class CoreEnginePart(EnginePartInterface):
    type = "core-engine"
    description = "core engine source"


class AWSEnginePluginPart(EnginePartInterface):
    type = "engine-plugin-aws"
    description = "default aws engine plugin"


class AzureEnginePluginPart(EnginePartInterface):
    type = "engine-plugin-azure"
    description = "default azure engine plugin"


class CMDBEnginePluginPart(EnginePartInterface):
    type = "engine-plugin-cmdb"
    description = "cmdb input engine plugin"


class WrapperEnginePart(EnginePartInterface):
    type = "engine-wrapper"
    description = "hamlet freemarker wrapper jar file"


class BashExecutorEnginePart(EnginePartInterface):
    type = "executor-bash"
    description = "bash based executor"
