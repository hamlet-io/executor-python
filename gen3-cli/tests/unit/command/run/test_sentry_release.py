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


@mock.patch('cot.command.run.sentry_release.run_sentry_release_backend')
def test_input_valid(run_sentry_release_backend):
    run_options_test(CliRunner(), run_sentry_release, ALL_VALID_OPTIONS, run_sentry_release_backend)
