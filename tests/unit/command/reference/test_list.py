import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.reference import list_reference_types, list_references
from hamlet.command.common.config import Options
from tests.unit.command.test_option_generation import (
    run_options_test,
)


info_mock_output = {
    "ReferenceTypes": [
        {
            "Type": "ReferenceType[1]",
            "Description": "ReferenceDescription[1]",
            "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
            "PluralType": "ReferencePluralType[1]",
        },
        {
            "Type": "ReferenceType[2]",
            "Description": "ReferenceDescription[2]",
            "Attributes": [{"Names": "Attribute[2]", "Types": ["string"]}],
            "PluralType": "ReferencePluralType[2]",
        },
    ],
    "ReferenceData": [
        {
            "Type": "ReferenceType[1]",
            "Id": "ReferenceDataId[1]",
            "Properties": {"ReferenceProperty[1]": "ReferencePropertyValue[1]"},
        },
        {
            "Type": "ReferenceType[2]",
            "Id": "ReferenceDataId[2]",
            "Properties": {"ReferenceProperty[2]": "ReferencePropertyValue[2]"},
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
def test_list_reference_types_input_valid(blueprint_mock):
    run_options_test(
        CliRunner(), list_reference_types, LIST_TYPES_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(info_mock_output)
def test_list_reference_types(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_reference_types, ["--output-format", "json"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Type": "ReferenceType[1]",
        "PluralType": "ReferencePluralType[1]",
        "Description": "ReferenceDescription[1]",
    } in result
    assert {
        "Type": "ReferenceType[2]",
        "PluralType": "ReferencePluralType[2]",
        "Description": "ReferenceDescription[2]",
    } in result


LIST_REFERENCES_VALID_OPTIONS = collections.OrderedDict()
LIST_REFERENCES_VALID_OPTIONS["-q,--query"] = "[]"
LIST_REFERENCES_VALID_OPTIONS["--output-format"] = "json"


@mock_backend(info_mock_output)
def test_list_references_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(), list_references, LIST_REFERENCES_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(info_mock_output)
def test_list_references(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_references, ["--output-format", "json"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {"Id": "ReferenceDataId[1]", "Type": "ReferenceType[1]"} in result
    assert {"Id": "ReferenceDataId[2]", "Type": "ReferenceType[2]"} in result
