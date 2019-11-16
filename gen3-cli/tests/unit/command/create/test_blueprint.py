import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.create.blueprint import blueprint as create_blueprint
from tests.unit.command.test_option_generation import (
    generate_test_options_collection,
    generate_incremental_required_options_collection
)


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'deployment_unit'
ALL_VALID_OPTIONS['-p,--generation-provider'] = 'generation_provider'
ALL_VALID_OPTIONS['-f,--generation-framework'] = 'generation_framework'
ALL_VALID_OPTIONS['-t,--generation-testcase'] = 'generation_testcase'
ALL_VALID_OPTIONS['-i,--generation-input-source'] = 'input-source'
ALL_VALID_OPTIONS['-s,--generation-scenarios'] = 'generation_scenarious'


@mock.patch('cot.command.create.template.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(create_blueprint.params)
    runner = CliRunner()

    for args in generate_incremental_required_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(create_blueprint, args)
        assert result.exit_code == 2, result.output
        assert subprocess_mock.run.call_count == 0

    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(create_blueprint, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
