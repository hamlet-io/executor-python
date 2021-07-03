import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.run.lambda_func import lambda_func as run_lambda_func
from tests.unit.command.test_option_generation import run_options_test


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-u,--deployment-unit"] = "unit"
ALL_VALID_OPTIONS["!-f,--function-id"] = "function_id"
ALL_VALID_OPTIONS["-i,--input-payload"] = "payload"
ALL_VALID_OPTIONS["-l,--include-log-tail"] = [True, False]


@mock.patch("hamlet.command.run.lambda_func.run_lambda_func_backend")
def test_input_valid(run_lambda_func_backend):
    run_options_test(
        CliRunner(), run_lambda_func, ALL_VALID_OPTIONS, run_lambda_func_backend.run
    )
