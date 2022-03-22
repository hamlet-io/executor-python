import os
import hashlib
import json
import tempfile

from unittest import mock

from click.testing import CliRunner
from hamlet.command.visual import list_diagrams as list_diagrams
from hamlet.command.visual import list_diagram_types as list_diagram_types


def template_backend_run_mock(data):
    def run(
        entrance="diagraminfo",
        entrance_parameter=None,
        output_filename="diagraminfo.json",
        output_dir=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        deployment_mode=None,
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
        info_filename = os.path.join(output_dir, output_filename)
        with open(info_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(info=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.context.Context")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, ContextClassMock, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(
                    hashlib.md5(str(info).encode()).hexdigest()
                )
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(info)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

        return wrapper

    return decorator


@mock_backend(
    {
        "Diagrams": [
            {
                "Id": "DiagramId[1]",
                "Type": "DiagramType[1]",
                "Description": "DiagramDescription[1]",
            },
            {
                "Id": "DiagramId[2]",
                "Type": "DiagramType[2]",
                "Description": "DiagramDescription[2]",
            },
        ]
    }
)
def test_query_list_diagrams(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(list_diagrams, ["--output-format", "json"])
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Id": "DiagramId[1]",
        "Type": "DiagramType[1]",
        "Description": "DiagramDescription[1]",
    } in result
    assert {
        "Id": "DiagramId[2]",
        "Type": "DiagramType[2]",
        "Description": "DiagramDescription[2]",
    } in result


@mock_backend(
    {
        "DiagramTypes": [
            {
                "Type": "DiagramType[1]",
                "Description": "DiagramDescription[1]",
            },
            {
                "Type": "DiagramType[2]",
                "Description": "DiagramDescription[2]",
            },
        ]
    }
)
def test_query_list_diagram_types(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(list_diagram_types, ["--output-format", "json"])
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {"Type": "DiagramType[1]", "Description": "DiagramDescription[1]"} in result
    assert {"Type": "DiagramType[2]", "Description": "DiagramDescription[2]"} in result
