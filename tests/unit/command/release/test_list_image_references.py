import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.release import list_image_references
from hamlet.command.common.config import Options
from tests.unit.command.test_option_generation import (
    run_options_test,
)


info_mock_output = {
    "Images": [
        {
            "Occurrence": "Occurrence[1]",
            "BUILD_FORMATS": "BUILD_FORMATS[1]",
            "BUILD_UNIT": "BUILD_UNIT[1]",
            "BUILD_REFERENCE": "BUILD_REFERENCE[1]",
            "APP_REFERENCE": "APP_REFERENCE[1]",
            "BUILD_SOURCE": "BUILD_SOURCE[1]",
        },
        {
            "Occurrence": "Occurrence[2]",
            "BUILD_FORMATS": "BUILD_FORMATS[2]",
            "BUILD_UNIT": "BUILD_UNIT[2]",
            "BUILD_REFERENCE": "BUILD_REFERENCE[2]",
            "APP_REFERENCE": "APP_REFERENCE[2]",
            "BUILD_SOURCE": "BUILD_SOURCE[2]",
        },
    ],
}


def template_backend_run_mock(data):
    def run(
        output_filename="imagedetails-config.json", output_dir=None, *args, **kwargs
    ):
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
def test_list_image_references_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(), list_image_references, LIST_TYPES_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(info_mock_output)
def test_list_image_references(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_image_references, ["--output-format", "json"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Occurrence": "Occurrence[1]",
        "BUILD_FORMATS": "BUILD_FORMATS[1]",
        "BUILD_UNIT": "BUILD_UNIT[1]",
        "BUILD_REFERENCE": "BUILD_REFERENCE[1]",
        "APP_REFERENCE": "APP_REFERENCE[1]",
        "BUILD_SOURCE": "BUILD_SOURCE[1]",
    } in result
    assert {
        "Occurrence": "Occurrence[2]",
        "BUILD_FORMATS": "BUILD_FORMATS[2]",
        "BUILD_UNIT": "BUILD_UNIT[2]",
        "BUILD_REFERENCE": "BUILD_REFERENCE[2]",
        "APP_REFERENCE": "APP_REFERENCE[2]",
        "BUILD_SOURCE": "BUILD_SOURCE[2]",
    } in result
