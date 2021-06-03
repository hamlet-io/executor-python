import os
from marshmallow import Schema, fields
from abc import ABC, abstractmethod


class EnginePartStateSchema(Schema):
    name = fields.String()
    description = fields.String()
    source_path = fields.String()
    source_name = fields.String()


class EnginePartInterface(ABC):

    type = None
    description = ''

    def __init__(self, source_name, source_path):
        self.source_path = source_path
        self.source_name = source_name


class CoreEnginePart(EnginePartInterface):
    type = 'core-engine'
    description = 'core engine source'


class AWSEnginePluginPart(EnginePartInterface):
    type = 'engine-plugin-aws'
    description = 'default aws engine plugin'


class AzureEnginePluginPart(EnginePartInterface):
    type = 'engine-plugin-azure'
    description = 'default azure engine plugin'


class CMDBEnginePluginPart(EnginePartInterface):
    type = 'engine-plugin-cmdb'
    description = 'cmdb input engine plugin'


class BinaryEnginePart(EnginePartInterface):
    type = 'engine-binary'
    description = 'cmdb input engine plugin'


class BashExecutorEnginePart(EnginePartInterface):
    type = 'executor-bash'
    description = 'bash based executor'
