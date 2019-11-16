import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.pipeline import pipeline as run_pipeline
from tests.unit.command.test_option_generation import run_options_test

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-i,--component'] = 'component'
ALL_VALID_OPTIONS['!-t,--tier'] = 'tier'
ALL_VALID_OPTIONS['-x,--instance'] = 'instance'
ALL_VALID_OPTIONS['-y,--version'] = 'version'
ALL_VALID_OPTIONS['-s,--pipeline-status-only'] = [True, False]
ALL_VALID_OPTIONS['-c,--pipeline-allow-concurrent'] = [True, False]


@mock.patch('cot.command.run.pipeline.subprocess')
def test_input_valid(subprocess_mock):
    run_options_test(CliRunner(), run_pipeline, ALL_VALID_OPTIONS, subprocess_mock)
