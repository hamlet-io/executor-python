import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.sentry_release import sentry_release as run_sentry_release
from tests.unit.command.test_option_generation import run_options_test

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-m,--sentry-source-map-s3-url'] = 'url'
ALL_VALID_OPTIONS['!-r,--sentry-release-name'] = 'release_name'
ALL_VALID_OPTIONS['-p,--sentry-url-prefix'] = 'url_prefix'
ALL_VALID_OPTIONS['-s,--run-setup'] = [True, False]


@mock.patch('cot.command.run.sentry_release.subprocess')
def test_input_valid(subprocess_mock):
    run_options_test(CliRunner(), run_sentry_release, ALL_VALID_OPTIONS, subprocess_mock)
