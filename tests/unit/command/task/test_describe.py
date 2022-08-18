import os
import json
import collections

from unittest import mock
from click.testing import CliRunner

from hamlet.command.task import describe_runbook
from hamlet.command.common.config import Options
from tests.unit.command.test_option_generation import (
    run_options_test,
)


runbookinfo_mock_output = {
    "RunBooks": [
        {
            "Name": "RunBook1",
            "Description": "RunBookDescription1",
            "Engine": "RunBookEngine1",
        },
        {
            "Name": "RunBook2",
            "Description": "RunBookDescription2",
            "Engine": "RunBookEngine2",
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


DECSCRIBE_RUNBOOK_VALID_OPTIONS = collections.OrderedDict()
DECSCRIBE_RUNBOOK_VALID_OPTIONS["!-n,--name"] = "RunBook1"
DECSCRIBE_RUNBOOK_VALID_OPTIONS["-q,--query"] = "[]"


@mock_backend(runbookinfo_mock_output)
def test_describe_runbook_input_valid(
    blueprint_mock,
):
    run_options_test(
        CliRunner(),
        describe_runbook,
        DECSCRIBE_RUNBOOK_VALID_OPTIONS,
        blueprint_mock.run,
    )


@mock_backend(runbookinfo_mock_output)
def test_describe_runbook(blueprint_mock):
    obj = Options()

    cli = CliRunner()
    result = cli.invoke(
        describe_runbook,
        ["--name", "RunBook1"],
        obj=obj,
    )
    print(result.output)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert {
        "Name": "RunBook1",
        "Description": "RunBookDescription1",
        "Engine": "RunBookEngine1",
    } == result
