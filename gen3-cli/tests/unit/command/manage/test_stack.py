import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.stack import stack as manage_stack
from tests.unit.command.test_option_generation import (
    generate_test_options_collection,
    generate_incremental_required_options_collection
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'unit'
ALL_VALID_OPTIONS['!-l,--level'] = [
    'account',
    'product',
    'segment',
    'solution',
    'application',
    'multiple'
]
ALL_VALID_OPTIONS['-d,--delete'] = [True, False]
ALL_VALID_OPTIONS['-i,--stack-initiate'] = [True, False]
ALL_VALID_OPTIONS['-m,--stack-monitor'] = [True, False]
ALL_VALID_OPTIONS['-n,--stack-name'] = 'name'
ALL_VALID_OPTIONS['-r,--region'] = 'region'
ALL_VALID_OPTIONS['-w,--stack-wait'] = 10
ALL_VALID_OPTIONS['-z,--deployment-unit-subset'] = 'subset'
ALL_VALID_OPTIONS['-y,--dryrun'] = [True, False]


@mock.patch('cot.command.manage.stack.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(manage_stack.params)
    runner = CliRunner()
    # testing that's impossible to run without full set of required options
    for args in generate_incremental_required_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(manage_stack, args)
        assert result.exit_code == 2, result.output
        assert subprocess_mock.run.call_count == 0

    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(manage_stack, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0


@mock.patch('cot.command.manage.stack.subprocess')
def test_input_validation(subprocess_mock):
    runner = CliRunner()
    # test level option
    result = runner.invoke(
        manage_stack,
        [
            '-u', 'unit',
            '-l', 'badlevelvalue'
        ],
    )
    assert result.exit_code == 2, result.output
    assert subprocess_mock.run.call_count == 0

    result = runner.invoke(
        manage_stack,
        [
            '-u', 'unit',
            '-l', 'segment'
        ],
    )
    assert result.exit_code == 0, result.output
    assert subprocess_mock.run.call_count == 1
    subprocess_mock.run.call_count = 0

    # test stack wait
    result = runner.invoke(
        manage_stack,
        [
            '-u', 'unit',
            '-l', 'segment',
            '-w', 'not an int'
        ],
    )
    assert result.exit_code == 2, result.output
    assert subprocess_mock.run.call_count == 0

    result = runner.invoke(
        manage_stack,
        [
            '-u', 'unit',
            '-l', 'segment',
            '-w', '10'
        ],
    )
    assert result.exit_code == 0, result.output
    assert subprocess_mock.run.call_count == 1
    subprocess_mock.run.call_count = 0
