import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.create.template import template as create_template
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'deployment_unit'
ALL_VALID_OPTIONS['!-l,--level'] = [
    "account",
    "segment",
    "solution",
    "application"
]
ALL_VALID_OPTIONS['-c,--config-ref'] = 'config_ref'
ALL_VALID_OPTIONS['-g,--resource-group'] = 'resource_group'
ALL_VALID_OPTIONS['-q,--request-ref'] = 'request_ref'
ALL_VALID_OPTIONS['-r,--region'] = 'region'
ALL_VALID_OPTIONS['-z,--deployment-unit-subset'] = 'deployment_unit_subset'
ALL_VALID_OPTIONS['-d,--deployment-mode'] = 'deployment_mode'
ALL_VALID_OPTIONS['-p,--generation-provider'] = 'generation_provider'
ALL_VALID_OPTIONS['-f,--generation-framework'] = 'generation_framework'
ALL_VALID_OPTIONS['-t,--generation-testcase'] = 'generation_testcase'
ALL_VALID_OPTIONS['-s,--generation-scenarios'] = 'generation_scenarios'
ALL_VALID_OPTIONS['-i,--generation-input-source'] = 'generation_input_source'


@mock.patch('cot.command.create.template.create_template_backend')
def test_input_valid(create_template_backend):
    run_options_test(CliRunner(), create_template, ALL_VALID_OPTIONS, create_template_backend)


@mock.patch('cot.command.create.template.create_template_backend')
def test_input_validation(create_template_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        create_template,
        create_template_backend,
        {
            '-u': 'unit',
            '-l': 'blueprint'
        },
        [
            ('-l', 'badlevelvalue', 'account')
        ]
    )
