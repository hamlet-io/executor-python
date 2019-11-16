import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.create.template import template as create_template
from tests.unit.command.test_option_generation import generate_test_options_collection


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['-c,--config-ref'] = 'config_ref'
ALL_VALID_OPTIONS['-g,--resource-group'] = 'resource_group'
ALL_VALID_OPTIONS['-l,--level'] = [
    "blueprint",
    "account",
    "segment",
    "solution",
    "application"
]
ALL_VALID_OPTIONS['-q,--request-ref'] = 'request_ref'
ALL_VALID_OPTIONS['-r,--region'] = 'region'
ALL_VALID_OPTIONS['-u,--deployment-unit'] = 'deployment_unit'
ALL_VALID_OPTIONS['-z,--deployment-unit-subset'] = 'deployment_unit_subset'
ALL_VALID_OPTIONS['-d,--deployment-mode'] = 'deployment_mode'
ALL_VALID_OPTIONS['-p,--generation-provider'] = 'generation_provider'
ALL_VALID_OPTIONS['-f,--generation-framework'] = 'generation_framework'
ALL_VALID_OPTIONS['-t,--generation-testcase'] = 'generation_testcase'
ALL_VALID_OPTIONS['-s,--generation-scenarios'] = 'generation_scenarios'
ALL_VALID_OPTIONS['-i,--generation-input-source'] = 'generation_input_source'


@mock.patch('cot.command.create.template.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(create_template.params)
    runner = CliRunner()
    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(create_template, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
