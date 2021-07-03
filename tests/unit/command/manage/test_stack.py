import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.manage.stack import stack as manage_stack
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-u,--deployment-unit"] = "unit"
ALL_VALID_OPTIONS["!-l,--deployment-group"] = "group"
ALL_VALID_OPTIONS["-d,--delete"] = [True, False]
ALL_VALID_OPTIONS["-i,--stack-initiate"] = [True, False]
ALL_VALID_OPTIONS["-m,--stack-monitor"] = [True, False]
ALL_VALID_OPTIONS["-r,--region"] = "region"
ALL_VALID_OPTIONS["-w,--stack-wait"] = 10
ALL_VALID_OPTIONS["-z,--deployment-unit-subset"] = "subset"
ALL_VALID_OPTIONS["-y,--dryrun"] = [True, False]


@mock.patch("hamlet.command.manage.stack.manage_stack_backend")
def test_input_valid(manage_stack_backend):
    run_options_test(
        CliRunner(), manage_stack, ALL_VALID_OPTIONS, manage_stack_backend.run
    )


@mock.patch("hamlet.command.manage.stack.manage_stack_backend")
def test_input_validation(manage_stack_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        manage_stack,
        manage_stack_backend.run,
        {"-u": "unit", "-l": "group"},
        [("-w", "not_an_int", 10)],
    )
