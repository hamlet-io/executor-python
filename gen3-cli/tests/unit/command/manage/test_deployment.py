import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.deployment import deployment as manage_deployment
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test

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
    run_options_test(CliRunner(), manage_deployment, ALL_VALID_OPTIONS, subprocess_mock)


@mock.patch('cot.command.manage.deployment.subprocess')
def test_input_validation(subprocess_mock):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        manage_deployment,
        subprocess_mock,
        {
            '-u': 'unit',
            '-l': 'segment'
        },
        [
            ('-l', 'badlevelvalue', 'segment'),
            ('-s', 'badscopevalue', 'resourceGroup'),
            ('-w', 'not_an_int', 10)
        ]
    )
