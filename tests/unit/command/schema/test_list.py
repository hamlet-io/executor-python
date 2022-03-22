import os
import hashlib
import json
import tempfile

from unittest import mock
from click.testing import CliRunner
from hamlet.command.schema import list_schemas
from hamlet.command.common.config import Options


def template_backend_run_mock(data):
    def run(
        entrance="schemalist",
        entrance_parameter=None,
        output_filename="schemalist-schemacontract.json",
        deployment_mode=None,
        output_dir=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        log_level=None,
        root_dir=None,
        district_type=None,
        tenant=None,
        account=None,
        product=None,
        environment=None,
        segment=None,
        engine=None,
    ):
        os.makedirs(output_dir, exist_ok=True)
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(schemalist=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.context.Context")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, ContextClassMock, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(
                    hashlib.md5(str(schemalist).encode()).hexdigest()
                )
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(schemalist)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

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
def test_query_list_schemas(blueprint_mock, ContextClassMock):
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
