import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.pipeline import pipeline as run_pipeline
from tests.unit.command.test_option_generation import (
    generate_test_options_collection,
    generate_incremental_required_options_collection
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-i,--component'] = 'component'
ALL_VALID_OPTIONS['!-t,--tier'] = 'tier'
ALL_VALID_OPTIONS['-x,--instance'] = 'instance'
ALL_VALID_OPTIONS['-y,--version'] = 'version'
ALL_VALID_OPTIONS['-s,--pipeline-status-only'] = [True, False]
ALL_VALID_OPTIONS['-c,--pipeline-allow-concurrent'] = [True, False]


@mock.patch('cot.command.run.pipeline.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(run_pipeline.params)
    runner = CliRunner()
    # testing that's impossible to run without full set of required options
    for args in generate_incremental_required_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_pipeline, args)
        assert result.exit_code == 2, result.output
        assert subprocess_mock.run.call_count == 0

    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_pipeline, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
