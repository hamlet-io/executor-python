import collections
import tempfile
import hashlib
import json
import os

from unittest import mock
from click.testing import CliRunner
from hamlet.command.deploy import run_deployments
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['-o,--output-dir'] = 'output_dir'
ALL_VALID_OPTIONS['-u,--deployment-unit'] = 'DeploymentUnit1'
ALL_VALID_OPTIONS['-l,--deployment-group'] = 'DeploymentGroup1'
ALL_VALID_OPTIONS['-m,--deployment-mode'] = 'deployment_mode'
ALL_VALID_OPTIONS['--refresh-outputs'] = True
ALL_VALID_OPTIONS['--confirm'] = True


def template_backend_run_mock(data):
    def run(
        entrance='unitlist',
        deployment_mode=None,
        output_dir=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        output_filename='unitlist-managementcontract.json'
    ):
        os.makedirs(output_dir, exist_ok=True)
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, 'wt+') as f:
            json.dump(data, f)
    return run


def mock_backend(unitlist=None):
    def decorator(func):
        @mock.patch('hamlet.command.deploy.manage_stack_backend')
        @mock.patch('hamlet.command.deploy.create_template_backend')
        @mock.patch('hamlet.backend.query.context.Context')
        @mock.patch('hamlet.backend.query.template')
        def wrapper(blueprint_mock, ContextClassMock, create_template_backend, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(hashlib.md5(str(unitlist).encode()).hexdigest())
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(unitlist)

                return func(blueprint_mock, ContextClassMock, create_template_backend, *args, **kwargs)

        return wrapper
    return decorator


unit_list = {
    'Stages': [
        {
            'Id': 'StageId1',
            'Steps': [
                {
                    'Id': 'StepId1',
                    'Parameters': {
                        'DeploymentUnit': 'DeploymentUnit1',
                        'DeploymentGroup': 'DeploymentGroup1',
                        'DeploymentProvider': 'aws',
                        'Operations': ['Operation11']
                    }
                },
                {
                    'Id': 'StepId2',
                    'Parameters': {
                        'DeploymentUnit': 'DeploymentUnit2',
                        'DeploymentGroup': 'DeploymentGroup2',
                        'DeploymentProvider': 'aws',
                        'Operations': ['Operation21']
                    }
                }
            ]
        }
    ]
}


@mock_backend(unit_list)
def test_input_valid(blueprint_mock, ContextClassMock, create_template_backend, manage_stack_backend):
    run_options_test(CliRunner(), run_deployments, ALL_VALID_OPTIONS, blueprint_mock.run)


@mock_backend(unit_list)
def test_input_validation(blueprint_mock, ContextClassMock, create_template_backend, manage_stack_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        run_deployments,
        create_template_backend.run,
        {
            '-m': 'DeploymentMode1',
            '-l': 'DeploymentGroup1',
            '-u': 'DeploymentUnit1',
        },
        []
    )
