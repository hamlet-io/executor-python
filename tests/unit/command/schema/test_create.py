import collections
import json
import os

from unittest import mock
from click.testing import CliRunner
from hamlet.command.schema import create_schemas as create_schemas
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-o,--output-dir"] = "output_dir"
ALL_VALID_OPTIONS["-s,--schema"] = "Schema1"


def template_backend_run_mock(data):
    def run(
        output_filename="schemalist-schemacontract.json",
        output_dir=None,
        *args,
        **kwargs
    ):
        os.makedirs(output_dir, exist_ok=True)
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(schemalist=None):
    def decorator(func):
        @mock.patch("hamlet.command.schema.create_template_backend")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, create_template_backend, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(schemalist)

            return func(blueprint_mock, create_template_backend, *args, **kwargs)

        return wrapper

    return decorator


schema_list = {
    "Stages": [
        {
            "Id": "StageId1",
            "Steps": [
                {
                    "Id": "StepId1",
                    "Parameters": {
                        "Schema": "Schema1",
                    },
                },
                {
                    "Id": "StepId2",
                    "Parameters": {
                        "Schema": "Schema2",
                    },
                },
            ],
        }
    ]
}


@mock_backend(schema_list)
def test_input_valid(blueprint_mock, create_template_backend):
    run_options_test(CliRunner(), create_schemas, ALL_VALID_OPTIONS, blueprint_mock.run)


@mock_backend(schema_list)
def test_input_validation(blueprint_mock, create_template_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        create_schemas,
        create_template_backend.run,
        {"-s": "Schema1", "-o": "."},
        [],
    )
