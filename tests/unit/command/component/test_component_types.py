import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.component.component_types import describe_component_type
from hamlet.command.common.config import Options
from tests.unit.command.test_option_generation import (
    run_options_test,
)


info_mock_output = {
    "ComponentTypes": [
        {
            "Type": "ComponentType[1]",
            "Description": "ComponentDescription[1]",
            "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
        },
        {
            "Type": "ComponentType[2]",
            "Description": "ComponentDescription[2]",
            "Attributes": [{"Names": "Attribute[2]", "Types": ["string"]}],
        },
    ],
}


def template_backend_run_mock(data):
    def run(output_filename="info.json", output_dir=None, *args, **kwargs):
        filename = os.path.join(output_dir, output_filename)
        if data:
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
DECSCRIBE_TYPE_VALID_OPTIONS["!-t,--type"] = "ComponentType[1]"
DECSCRIBE_TYPE_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(info_mock_output)
def test_describe_component_type_input_valid(blueprint_mock):
    run_options_test(
        CliRunner(),
        describe_component_type,
        DECSCRIBE_TYPE_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(info_mock_output)
def test_describe_component_type(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        describe_component_type, ["--type", "ComponentType[1]"], obj=obj
    )
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert {
        "Type": "ComponentType[1]",
        "Description": "ComponentDescription[1]",
        "Attributes": [{"Names": "Attribute[1]", "Types": ["string"]}],
    } == result
