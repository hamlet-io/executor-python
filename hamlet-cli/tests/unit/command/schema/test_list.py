import os
import hashlib
import json
import tempfile

from unittest import mock
from click.testing import CliRunner
from hamlet.command.schema import list_schemas
from hamlet.command.common.context import Generation


def template_backend_run_mock(data):
    def run(
        entrance='schemaset',
        deployment_mode=None,
        output_dir=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        output_filename='schemaset-schemacontract.json'
    ):
        os.makedirs(output_dir, exist_ok=True)
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, 'wt+') as f:
            json.dump(data, f)
    return run


def mock_backend(schemaset=None):
    def decorator(func):
        @mock.patch('hamlet.backend.query.context.Context')
        @mock.patch('hamlet.backend.query.template')
        def wrapper(blueprint_mock, ContextClassMock, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(hashlib.md5(str(schemaset).encode()).hexdigest())
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(schemaset)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

        return wrapper
    return decorator


@mock_backend(
    {
        'Stages': [
            {
                'Id': 'StageId[1]',
                'Steps': [
                    {
                        'Id': 'StepId[1]',
                        'Parameters': {
                            'DeploymentUnit': 'DeploymentUnit[1]',
                            'DeploymentGroup': 'DeploymentGroup[1]',
                            'DeploymentProvider': 'DeploymentProvider[1]',
                        }
                    },
                    {
                        'Id': 'StepId[2]',
                        'Parameters': {
                            'DeploymentUnit': 'DeploymentUnit[2]',
                            'DeploymentGroup': 'DeploymentGroup[2]',
                            'DeploymentProvider': 'DeploymentProvider[2]',
                        }
                    }
                ]
            },
            {
                'Id': 'StageId[2]',
                'Steps': [
                    {
                        'Id': 'StepId[3]',
                        'Parameters': {
                            'DeploymentUnit': 'DeploymentUnit[3]',
                            'DeploymentGroup': 'DeploymentGroup[3]',
                            'DeploymentProvider': 'DeploymentProvider[3]',
                        }
                    },
                    {
                        'Id': 'StepId[4]',
                        'Parameters': {
                            'DeploymentUnit': 'DeploymentUnit[4]',
                            'DeploymentGroup': 'DeploymentGroup[4]',
                            'DeploymentProvider': 'DeploymentProvider[4]',
                        }
                    }
                ]
            }
        ]
    }
)
def test_query_list_schemas(blueprint_mock, ContextClassMock):
    obj = Generation()

    cli = CliRunner()
    result = cli.invoke(
        list_schemas,
        [
            '--output-format', 'json'
        ],
        obj=obj
    )
    print(result.output)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 4
    assert {
        'Instance': 'DeploymentUnit[1]',
        'Type': 'DeploymentGroup[1]',
    } in result
    assert {
        'Instance': 'DeploymentUnit[2]',
        'Type': 'DeploymentGroup[2]',
    } in result
    assert {
        'Instance': 'DeploymentUnit[3]',
        'Type': 'DeploymentGroup[3]',
    } in result
    assert {
        'Instance': 'DeploymentUnit[4]',
        'Type': 'DeploymentGroup[4]',
    } in result
