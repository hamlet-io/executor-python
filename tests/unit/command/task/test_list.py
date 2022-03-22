import os
import hashlib
import json
import tempfile
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
        entrance="runbookinfo",
        entrance_parameter=None,
        output_filename="runbookinfo-config.json",
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


LIST_RUNBOOKS_VALID_OPTIONS = collections.OrderedDict()
LIST_RUNBOOKS_VALID_OPTIONS["-q,--query"] = "[]"
LIST_RUNBOOKS_VALID_OPTIONS["--output-format"] = "json"


@mock_backend(runbookinfo_mock_output)
def test_list_runbooks_input_valid(
    blueprint_mock,
    ContextClassMock,
):
    run_options_test(
        CliRunner(), list_runbooks, LIST_RUNBOOKS_VALID_OPTIONS, blueprint_mock.run
    )


@mock_backend(runbookinfo_mock_output)
def test_list_runbooks(blueprint_mock, ContextClassMock):
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
