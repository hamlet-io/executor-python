import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.task import list_runbooks
from hamlet.command.common.config import Options
from tests.unit.command.test_option_generation import (
    run_options_test,
)


runbookinfo_mock_output = {
    "RunBooks": [
        {
            "Name": "RunBook[1]",
            "Description": "RunBookDescription[1]",
            "Engine": "RunBookEngine[1]",
        },
        {
            "Name": "RunBook[2]",
            "Description": "RunBookDescription[2]",
            "Engine": "RunBookEngine[2]",
        },
    ],
}


def template_backend_run_mock(data):
    def run(
        output_filename="runbookinfo-config.json", output_dir=None, *args, **kwargs
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


LIST_RUNBOOKS_VALID_OPTIONS = collections.OrderedDict()
LIST_RUNBOOKS_VALID_OPTIONS["-q,--query"] = "[]"
LIST_RUNBOOKS_VALID_OPTIONS["--output-format"] = "json"


@mock_backend(runbookinfo_mock_output)
def test_list_runbooks_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(), list_runbooks, LIST_RUNBOOKS_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(runbookinfo_mock_output)
def test_list_runbooks(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(list_runbooks, ["--output-format", "json"], obj=obj)
    print(result.exc_info)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Name": "RunBook[1]",
        "Description": "RunBookDescription[1]",
        "Engine": "RunBookEngine[1]",
    } in result
    assert {
        "Name": "RunBook[2]",
        "Description": "RunBookDescription[2]",
        "Engine": "RunBookEngine[2]",
    } in result
