import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.layer import list_layers, list_layer_types
from hamlet.command.common.config import Options
from tests.unit.command.test_option_generation import (
    run_options_test,
)


info_mock_output = {
    "LayerTypes": [
        {
            "Type": "LayerType[1]",
            "Description": "LayerDescription[1]",
            "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
            "ReferenceLookupType": "LayerReferenceLookupType[1]",
        },
        {
            "Type": "LayerType[2]",
            "Description": "LayerDescription[2]",
            "Attributes": [{"Names": "Attribute[2]", "Types": ["string"]}],
            "ReferenceLookupType": "LayerReferenceLookupType[2]",
        },
    ],
    "LayerData": [
        {
            "Type": "LayerType[1]",
            "Id": "LayerDataId[1]",
            "Name": "LayerDataName[1]",
            "Properties": {"LayerProperty[1]": "LayerPropertyValue[1]"},
        },
        {
            "Type": "LayerType[2]",
            "Id": "LayerDataId[2]",
            "Name": "LayerDataName[2]",
            "Properties": {"LayerProperty[2]": "LayerPropertyValue[2]"},
        },
    ],
}


def template_backend_run_mock(data):
    def run(output_filename="info.json", output_dir=None, *args, **kwargs):
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, output_filename)
        with open(filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(data=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(data)
            return func(blueprint_mock, *args, **kwargs)

        return wrapper

    return decorator


LIST_TYPES_VALID_OPTIONS = collections.OrderedDict()
LIST_TYPES_VALID_OPTIONS["-q,--query"] = "[]"
LIST_TYPES_VALID_OPTIONS["--output-format"] = "json"


@mock_backend(info_mock_output)
def test_list_layer_types_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(), list_layer_types, LIST_TYPES_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(info_mock_output)
def test_list_layer_types(
    blueprint_mock,
):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_layer_types, ["--output-format", "json"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Type": "LayerType[1]",
        "ReferenceLookupType": "LayerReferenceLookupType[1]",
        "Description": "LayerDescription[1]",
    } in result
    assert {
        "Type": "LayerType[2]",
        "ReferenceLookupType": "LayerReferenceLookupType[2]",
        "Description": "LayerDescription[2]",
    } in result


LIST_LAYERS_VALID_OPTIONS = collections.OrderedDict()
LIST_LAYERS_VALID_OPTIONS["-q,--query"] = "[]"
LIST_LAYERS_VALID_OPTIONS["--output-format"] = "json"


@mock_backend(info_mock_output)
def test_list_layers_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(), list_layers, LIST_LAYERS_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(info_mock_output)
def test_list_layers(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_layers, ["--output-format", "json"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Id": "LayerDataId[1]",
        "Name": "LayerDataName[1]",
        "Active": None,
        "Type": "LayerType[1]",
    } in result
    assert {
        "Id": "LayerDataId[2]",
        "Name": "LayerDataName[2]",
        "Active": None,
        "Type": "LayerType[2]",
    } in result
