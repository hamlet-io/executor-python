import collections
import json
import os

from unittest import mock
from click.testing import CliRunner
from hamlet.command.deploy.run import run_deployments
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["-o,--output-dir"] = "output_dir"
ALL_VALID_OPTIONS["-u,--deployment-unit"] = "DeploymentUnit1"
ALL_VALID_OPTIONS["-l,--deployment-group"] = "DeploymentGroup1"
ALL_VALID_OPTIONS["-m,--deployment-mode"] = "deployment_mode"
ALL_VALID_OPTIONS["-s,--deployment-state"] = "deployed"
ALL_VALID_OPTIONS["--refresh-outputs"] = True
ALL_VALID_OPTIONS["--confirm"] = True
ALL_VALID_OPTIONS["--dryrun"] = True


def template_backend_run_mock(data):
    def run(
        output_filename="unitlist-managementcontract.json",
        output_dir=None,
        *args,
        **kwargs
    ):
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, output_filename)
        with open(filepath, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(unitlist=None):
    def decorator(func):
        @mock.patch("hamlet.command.deploy.run.run_deployment")
        @mock.patch("hamlet.command.deploy.run.create_deployment")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(
            blueprint_mock,
            create_deployment_backend,
            run_deployment_backend,
            *args,
            **kwargs
        ):
            blueprint_mock.run.side_effect = template_backend_run_mock(unitlist)

            return func(
                blueprint_mock,
                create_deployment_backend,
                run_deployment_backend,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


unit_list = {
    "Stages": [
        {
            "Id": "StageId1",
            "Steps": [
                {
                    "Id": "StepId1",
                    "Parameters": {
                        "DeploymentUnit": "DeploymentUnit1",
                        "DeploymentGroup": "DeploymentGroup1",
                        "DeploymentProvider": "aws",
                        "Operations": ["Operation11"],
                        "CurrentState": "deployed",
                    },
                },
                {
                    "Id": "StepId2",
                    "Parameters": {
                        "DeploymentUnit": "DeploymentUnit2",
                        "DeploymentGroup": "DeploymentGroup2",
                        "DeploymentProvider": "aws",
                        "Operations": ["Operation2"],
                        "CurrentState": "deployed",
                    },
                },
            ],
        }
    ]
}


@mock_backend(unit_list)
def test_input_valid(blueprint_mock, create_deployment_backend, run_deployment_backend):
    run_options_test(
        CliRunner(), run_deployments, ALL_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(unit_list)
def test_input_validation(
    blueprint_mock, create_deployment_backend, run_deployment_backend
):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        run_deployments,
        create_deployment_backend.run,
        {
            "-m": "DeploymentMode1",
            "-l": "DeploymentGroup1",
            "-u": "DeploymentUnit1",
            "-s": "deployed",
        },
        [],
    )
