import os
import hashlib
import json
import tempfile
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
        entrance="imagedetails",
        entrance_parameter=None,
        output_filename="imagedetails-config.json",
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


LIST_TYPES_VALID_OPTIONS = collections.OrderedDict()
LIST_TYPES_VALID_OPTIONS["-q,--query"] = "[]"
LIST_TYPES_VALID_OPTIONS["--output-format"] = "json"


@mock_backend(info_mock_output)
def test_list_image_references_input_valid(
    blueprint_mock,
    ContextClassMock,
):
    run_options_test(
        CliRunner(), list_image_references, LIST_TYPES_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(info_mock_output)
def test_list_image_references(blueprint_mock, ContextClassMock):
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
