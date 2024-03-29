import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.layer import describe_layer_type, describe_layer
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


DECSCRIBE_TYPE_VALID_OPTIONS = collections.OrderedDict()
DECSCRIBE_TYPE_VALID_OPTIONS["!-t,--type"] = "ReferenceType[1]"
DECSCRIBE_TYPE_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_describe_layer_type_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(),
        describe_layer_type,
        DECSCRIBE_TYPE_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_describe_layer_type(
    blueprint_mock,
):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(describe_layer_type, ["--type", "LayerType[1]"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert {
        "Type": "LayerType[1]",
        "Description": "LayerDescription[1]",
        "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
        "ReferenceLookupType": "LayerReferenceLookupType[1]",
    } == result


DECSCRIBE_LAYER_VALID_OPTIONS = collections.OrderedDict()
DECSCRIBE_LAYER_VALID_OPTIONS["!-t,--type"] = "LayerType[1]"
DECSCRIBE_LAYER_VALID_OPTIONS["!-n,--name"] = "LayerDataName[1]"
DECSCRIBE_LAYER_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_describe_layer_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(),
        describe_layer,
        DECSCRIBE_LAYER_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_describe_layer(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        describe_layer,
        ["--type", "LayerType[1]", "--name", "LayerDataName[1]"],
        obj=obj,
    )
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert {
        "Type": "LayerType[1]",
        "Id": "LayerDataId[1]",
        "Name": "LayerDataName[1]",
        "Properties": {"LayerProperty[1]": "LayerPropertyValue[1]"},
    } == result
