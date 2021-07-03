import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.run.pipeline import pipeline as run_pipeline
from tests.unit.command.test_option_generation import run_options_test

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-i,--component"] = "component"
ALL_VALID_OPTIONS["!-t,--tier"] = "tier"
ALL_VALID_OPTIONS["-x,--instance"] = "instance"
ALL_VALID_OPTIONS["-y,--version"] = "version"
ALL_VALID_OPTIONS["-s,--pipeline-status-only"] = [True, False]
ALL_VALID_OPTIONS["-c,--pipeline-allow-concurrent"] = [True, False]


@mock.patch("hamlet.command.run.pipeline.run_pipeline_backend")
def test_input_valid(run_pipeline_backend):
    run_options_test(
        CliRunner(), run_pipeline, ALL_VALID_OPTIONS, run_pipeline_backend.run
    )
