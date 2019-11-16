import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.sentry_release import sentry_release as run_sentry_release
from tests.unit.command.test_option_generation import (
    generate_test_options_collection,
    generate_incremental_required_options_collection
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-m,--sentry-source-map-s3-url'] = 'url'
ALL_VALID_OPTIONS['!-r,--sentry-release-name'] = 'release_name'
ALL_VALID_OPTIONS['-p,--sentry-url-prefix'] = 'url_prefix'
ALL_VALID_OPTIONS['-s,--run-setup'] = [True, False]


@mock.patch('cot.command.run.sentry_release.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(run_sentry_release.params)
    runner = CliRunner()
    # testing that's impossible to run without full set of required options
    for args in generate_incremental_required_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_sentry_release, args)
        assert result.exit_code == 2, result.output
        assert subprocess_mock.run.call_count == 0

    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_sentry_release, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
