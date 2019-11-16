import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.deployment import deployment as manage_deployment
from tests.unit.command.test_option_generation import generate_test_options_collection


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
ALL_VALID_OPTIONS['-i,--deployment-initiate'] = [True, False]
ALL_VALID_OPTIONS['-m,--deployment-monitor'] = [True, False]
ALL_VALID_OPTIONS['-n,--deployment-name'] = 'name'
ALL_VALID_OPTIONS['-r,--region'] = 'region'
ALL_VALID_OPTIONS['-s,--deployment-scope'] = [
    'subscription',
    'resourceGroup'
]
ALL_VALID_OPTIONS['-w,--deployment-wait'] = 10
ALL_VALID_OPTIONS['-z,--deployment-unit-subset'] = 'subset'


@mock.patch('cot.command.manage.deployment.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(manage_deployment.params)
    runner = CliRunner()
    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(manage_deployment, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0


@mock.patch('cot.command.manage.deployment.subprocess')
def test_input_validation(subprocess_mock):
    runner = CliRunner()
    # test level option
    result = runner.invoke(
        manage_deployment,
        [
            '-u', 'unit',
            '-l', 'badlevelvalue'
        ],
    )
    assert result.exit_code == 2, result.output
    assert subprocess_mock.run.call_count == 0

    result = runner.invoke(
        manage_deployment,
        [
            '-u', 'unit',
            '-l', 'segment'
        ],
    )
    assert result.exit_code == 0, result.output
    assert subprocess_mock.run.call_count == 1
    subprocess_mock.run.call_count = 0
    # test deployment scope option
    result = runner.invoke(
        manage_deployment,
        [
            '-u', 'unit',
            '-l', 'segment',
            '-s', 'sfafs'
        ],
    )
    assert result.exit_code == 2, result.output
    assert subprocess_mock.run.call_count == 0

    result = runner.invoke(
        manage_deployment,
        [
            '-u', 'unit',
            '-l', 'segment',
            '-s', 'resourceGroup'
        ],
    )
    assert result.exit_code == 0, result.output
    assert subprocess_mock.run.call_count == 1
    subprocess_mock.run.call_count = 0
    # test deployment wait
    result = runner.invoke(
        manage_deployment,
        [
            '-u', 'unit',
            '-l', 'segment',
            '-w', 'not an int'
        ],
    )
    assert result.exit_code == 2, result.output
    assert subprocess_mock.run.call_count == 0

    result = runner.invoke(
        manage_deployment,
        [
            '-u', 'unit',
            '-l', 'segment',
            '-w', '10'
        ],
    )
    assert result.exit_code == 0, result.output
    assert subprocess_mock.run.call_count == 1
    subprocess_mock.run.call_count = 0
