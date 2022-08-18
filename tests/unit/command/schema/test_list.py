import os
import json

from unittest import mock
from click.testing import CliRunner
from hamlet.command.schema import list_schemas
from hamlet.command.common.config import Options


def template_backend_run_mock(data):
    def run(
        output_filename="schemalist-schemacontract.json",
        output_dir=None,
        *args,
        **kwargs
    ):
        os.makedirs(output_dir, exist_ok=True)
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(schemalist=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(schemalist)
            return func(blueprint_mock, *args, **kwargs)

        return wrapper

    return decorator


@mock_backend(
    {
        "Stages": [
            {
                "Id": "StageId1",
                "Steps": [
                    {
                        "Id": "StepId1",
                        "Parameters": {"Schema": "Schema1"},
                    },
                    {
                        "Id": "StepId2",
                        "Parameters": {"Schema": "Schema2"},
                    },
                ],
            },
            {
                "Id": "StageId2",
                "Steps": [
                    {
                        "Id": "StepId3",
                        "Parameters": {"Schema": "Schema3"},
                    },
                    {
                        "Id": "StepId4",
                        "Parameters": {"Schema": "Schema4"},
                    },
                ],
            },
        ]
    }
)
def test_query_list_schemas(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_schemas, ["--output-format", "json"], obj=obj)
    print(result.output)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 4
    assert {
        "Schema": "Schema1",
    } in result
    assert {
        "Schema": "Schema2",
    } in result
    assert {
        "Schema": "Schema3",
    } in result
    assert {
        "Schema": "Schema4",
    } in result
