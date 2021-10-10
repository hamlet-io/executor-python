import os
import hashlib
import json
import tempfile
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.reference import describe_reference_type, describe_reference
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
    def run(
        entrance="info",
        output_filename="info.json",
        deployment_mode=None,
        output_dir=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        log_level=None,
        root_dir=None,
        tenant=None,
        account=None,
        product=None,
        environment=None,
        segment=None,
    ):
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, output_filename)
        with open(filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(data=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.context.Context")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, ContextClassMock, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(
                    hashlib.md5(str(data).encode()).hexdigest()
                )
                ContextObjectMock.cache_dir = temp_cache_dir
                blueprint_mock.run.side_effect = template_backend_run_mock(data)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

        return wrapper

    return decorator


DECSCRIBE_TYPE_VALID_OPTIONS = collections.OrderedDict()
DECSCRIBE_TYPE_VALID_OPTIONS["!-t,--type"] = "ReferenceType[1]"
DECSCRIBE_TYPE_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_describe_reference_type_input_valid(
    blueprint_mock,
    ContextClassMock,
):
    run_options_test(
        CliRunner(),
        describe_reference_type,
        DECSCRIBE_TYPE_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_describe_reference_type(blueprint_mock, ContextClassMock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        describe_reference_type, ["--type", "ReferenceType[1]"], obj=obj
    )
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert {
        "Type": "ReferenceType[1]",
        "Description": "ReferenceDescription[1]",
        "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
        "PluralType": "ReferencePluralType[1]",
    } == result


DECSCRIBE_REFERENCE_VALID_OPTIONS = collections.OrderedDict()
DECSCRIBE_REFERENCE_VALID_OPTIONS["!-t,--type"] = "ReferenceType[1]"
DECSCRIBE_REFERENCE_VALID_OPTIONS["!-i,--id"] = "ReferenceDataId[1]"
DECSCRIBE_REFERENCE_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_describe_reference_input_valid(
    blueprint_mock,
    ContextClassMock,
):
    run_options_test(
        CliRunner(),
        describe_reference,
        DECSCRIBE_REFERENCE_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_describe_reference(blueprint_mock, ContextClassMock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        describe_reference,
        ["--type", "ReferenceType[1]", "--id", "ReferenceDataId[1]"],
        obj=obj,
    )
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert {
        "Type": "ReferenceType[1]",
        "Id": "ReferenceDataId[1]",
        "Properties": {"ReferenceProperty[1]": "ReferencePropertyValue[1]"},
    } == result
