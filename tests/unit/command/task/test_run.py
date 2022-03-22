import collections
import tempfile
import hashlib
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
    def run(
        entrance=None,
        entrance_parameter=None,
        output_filename=None,
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
        for set in data:
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, set[2])
            with open(filename, "wt+") as f:
                json.dump(set[0], f)

    return run


def mock_backend(runbookinfo=None, contract=None):
    def decorator(func):
        @mock.patch("hamlet.command.task.contract_backend")
        @mock.patch("hamlet.backend.query.context.Context")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(
            blueprint_mock, ContextClassMock, contract_backend, *args, **kwargs
        ):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(
                    hashlib.md5(str(runbookinfo).encode()).hexdigest()
                )
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(
                    [
                        (runbookinfo, "runbookinfo", "runbookinfo-config.json"),
                        (contract, "runbook", "runbook-contract.json"),
                    ]
                )

                return func(
                    blueprint_mock, ContextClassMock, contract_backend, *args, **kwargs
                )

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
def test_input_valid(blueprint_mock, ContextClassMock, contract_backend):
    run_options_test(CliRunner(), run_runbook, ALL_VALID_OPTIONS, contract_backend.run)


@mock_backend(runbookinfo_mock_output, runbook_mock_output)
def test_input_validation(blueprint_mock, ContextClassMock, contract_backend):
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
