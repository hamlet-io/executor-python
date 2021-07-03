import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.manage.deployment import deployment as manage_deployment
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-u,--deployment-unit"] = "unit"
ALL_VALID_OPTIONS["!-l,--deployment-group"] = "group"
ALL_VALID_OPTIONS["-d,--delete"] = [True, False]
ALL_VALID_OPTIONS["-g,--resource-group"] = "group"
ALL_VALID_OPTIONS["-i,--deployment-initiate"] = [True, False]
ALL_VALID_OPTIONS["-m,--deployment-monitor"] = [True, False]
ALL_VALID_OPTIONS["-r,--region"] = "region"
ALL_VALID_OPTIONS["-s,--deployment-scope"] = ["subscription", "resourceGroup"]
ALL_VALID_OPTIONS["-w,--deployment-wait"] = 10
ALL_VALID_OPTIONS["-z,--deployment-unit-subset"] = "subset"


@mock.patch("hamlet.command.manage.deployment.manage_deployment_backend")
def test_input_valid(manage_deployment_backend):
    run_options_test(
        CliRunner(), manage_deployment, ALL_VALID_OPTIONS, manage_deployment_backend.run
    )


@mock.patch("hamlet.command.manage.deployment.manage_deployment_backend")
def test_input_validation(manage_deployment_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        manage_deployment,
        manage_deployment_backend.run,
        {"-u": "unit", "-l": "group"},
        [("-s", "badscopevalue", "resourceGroup"), ("-w", "not_an_int", 10)],
    )
