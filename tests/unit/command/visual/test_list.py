import os
import json

from unittest import mock

from click.testing import CliRunner
from hamlet.command.visual import list_diagrams as list_diagrams
from hamlet.command.visual import list_diagram_types as list_diagram_types


def template_backend_run_mock(data):
    def run(output_filename="diagraminfo.json", output_dir=None, *args, **kwargs):
        os.makedirs(output_dir, exist_ok=True)
        info_filename = os.path.join(output_dir, output_filename)
        with open(info_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(info=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(info)
            return func(blueprint_mock, *args, **kwargs)

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
def test_query_list_diagrams(blueprint_mock):
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
def test_query_list_diagram_types(blueprint_mock):
    cli = CliRunner()
    result = cli.invoke(list_diagram_types, ["--output-format", "json"])
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {"Type": "DiagramType[1]", "Description": "DiagramDescription[1]"} in result
    assert {"Type": "DiagramType[2]", "Description": "DiagramDescription[2]"} in result
