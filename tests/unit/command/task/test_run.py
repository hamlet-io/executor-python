import collections
import json
import os

from unittest import mock
from click.testing import CliRunner
from hamlet.command.task import run_runbook
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-n,--name"] = "RunBook1"
ALL_VALID_OPTIONS["--confirm"] = False
ALL_VALID_OPTIONS["--silent"] = False
ALL_VALID_OPTIONS["--"] = "test=true"


def template_backend_run_mock(data):
    def run(output_filename=None, output_dir=None, *args, **kwargs):
        for set in data:
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, set[2])
            with open(filename, "wt+") as f:
                json.dump(set[0], f)

    return run


def mock_backend(runbookinfo=None, contract=None):
    def decorator(func):
        @mock.patch("hamlet.command.task.contract_backend")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, contract_backend, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(
                [
                    (runbookinfo, "runbookinfo", "runbookinfo-config.json"),
                    (contract, "runbook", "runbook-contract.json"),
                ]
            )

            return func(blueprint_mock, contract_backend, *args, **kwargs)

        return wrapper

    return decorator


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

runbook_mock_output = {"Stages": [{"Id": "Stage1", "Steps": [{"Id": "Step1"}]}]}


@mock_backend(runbookinfo_mock_output, runbook_mock_output)
def test_input_valid(blueprint_mock, contract_backend):
    run_options_test(CliRunner(), run_runbook, ALL_VALID_OPTIONS, contract_backend.run)


@mock_backend(runbookinfo_mock_output, runbook_mock_output)
def test_input_validation(blueprint_mock, contract_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        run_runbook,
        contract_backend.run,
        {
            "-n": "RunBook1",
        },
        [],
    )
