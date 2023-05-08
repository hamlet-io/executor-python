import os
import json
from unittest import mock
from click.testing import CliRunner
from hamlet.command.deploy.list import list_deployments


def template_backend_run_mock(data):
    def run(
        output_filename="unitlist-managementcontract.json",
        output_dir=None,
        *args,
        **kwargs
    ):
        os.makedirs(output_dir, exist_ok=True)
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(unitlist=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(unitlist)

            return func(blueprint_mock, *args, **kwargs)

        return wrapper

    return decorator


@mock_backend(
    {
        "Stages": [
            {
                "Id": "StageId[1]",
                "Steps": [
                    {
                        "Id": "StepId[1]",
                        "Parameters": {
                            "DeploymentUnit": "DeploymentUnit[1]",
                            "DeploymentGroup": "DeploymentGroup[1]",
                            "DeploymentProvider": "DeploymentProvider[1]",
                            "Operations": ["Operation[1]"],
                            "CurrentState": "deployed",
                        },
                    },
                    {
                        "Id": "StepId[2]",
                        "Parameters": {
                            "DeploymentUnit": "DeploymentUnit[2]",
                            "DeploymentGroup": "DeploymentGroup[2]",
                            "DeploymentProvider": "DeploymentProvider[2]",
                            "Operations": ["Operation[2]"],
                            "CurrentState": "deployed",
                        },
                    },
                ],
            },
            {
                "Id": "StageId[2]",
                "Steps": [
                    {
                        "Id": "StepId[3]",
                        "Parameters": {
                            "DeploymentUnit": "DeploymentUnit[3]",
                            "DeploymentGroup": "DeploymentGroup[3]",
                            "DeploymentProvider": "DeploymentProvider[3]",
                            "Operations": ["Operation[3]"],
                            "CurrentState": "deployed",
                        },
                    },
                    {
                        "Id": "StepId[4]",
                        "Parameters": {
                            "DeploymentUnit": "DeploymentUnit[4]",
                            "DeploymentGroup": "DeploymentGroup[4]",
                            "DeploymentProvider": "DeploymentProvider[4]",
                            "Operations": ["Operation[4]"],
                            "CurrentState": "deployed",
                        },
                    },
                ],
            },
        ]
    }
)
def test_query_list_deployments(blueprint_mock):
    cli = CliRunner()
    result = cli.invoke(list_deployments, ["--output-format", "json"])
    print(result.output)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 4
    assert {
        "DeploymentUnit": "DeploymentUnit[1]",
        "DeploymentGroup": "DeploymentGroup[1]",
        "DeploymentProvider": "DeploymentProvider[1]",
        "Operations": ["Operation[1]"],
        "CurrentState": "deployed",
    } in result
    assert {
        "DeploymentUnit": "DeploymentUnit[2]",
        "DeploymentGroup": "DeploymentGroup[2]",
        "DeploymentProvider": "DeploymentProvider[2]",
        "Operations": ["Operation[2]"],
        "CurrentState": "deployed",
    } in result
    assert {
        "DeploymentUnit": "DeploymentUnit[3]",
        "DeploymentGroup": "DeploymentGroup[3]",
        "DeploymentProvider": "DeploymentProvider[3]",
        "Operations": ["Operation[3]"],
        "CurrentState": "deployed",
    } in result
    assert {
        "DeploymentUnit": "DeploymentUnit[4]",
        "DeploymentGroup": "DeploymentGroup[4]",
        "DeploymentProvider": "DeploymentProvider[4]",
        "Operations": ["Operation[4]"],
        "CurrentState": "deployed",
    } in result
