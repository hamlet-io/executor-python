import os
import hashlib
import json
import tempfile
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.reference import query_reference_types, query_references
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
        entrance_parameter=None,
        output_filename="info.json",
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


QUERY_TYPES_VALID_OPTIONS = collections.OrderedDict()
QUERY_TYPES_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_query_reference_types_input_valid(
    blueprint_mock,
    ContextClassMock,
):
    run_options_test(
        CliRunner(),
        query_reference_types,
        QUERY_TYPES_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_query_reference_types(blueprint_mock, ContextClassMock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        query_reference_types, ["--query", "[?Type==`ReferenceType[1]`]"], obj=obj
    )
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 1
    assert {
        "Type": "ReferenceType[1]",
        "Description": "ReferenceDescription[1]",
        "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
        "PluralType": "ReferencePluralType[1]",
    } in result


QUERY_REFERENCES_VALID_OPTIONS = collections.OrderedDict()
QUERY_REFERENCES_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_query_references_input_valid(
    blueprint_mock,
    ContextClassMock,
):
    run_options_test(
        CliRunner(),
        query_references,
        QUERY_REFERENCES_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_query_references(blueprint_mock, ContextClassMock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        query_references,
        ["--query", "[?Id==`ReferenceDataId[1]`]"],
        obj=obj,
    )
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 1
    assert {
        "Type": "ReferenceType[1]",
        "Id": "ReferenceDataId[1]",
        "Properties": {"ReferenceProperty[1]": "ReferencePropertyValue[1]"},
    } in result
