from unittest import mock
from click.testing import CliRunner
from hamlet.command.deploy import run_deployments as run_deployments
from tests.unit.command.test_option_generation import run_validatable_option_test


@mock.patch('hamlet.command.deploy.create_template_backend')
@mock.patch('hamlet.command.deploy.manage_stack_backend')
def test_input_validation(create_template_backend, manage_stack_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        run_deployments,
        create_template_backend.run,
        {
            '-l': 'segment',
            '-u': 'baseline'
        },
        []
    )
