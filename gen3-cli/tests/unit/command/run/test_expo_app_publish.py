import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.expo_app_publish import expo_app_publish as run_expo_app_publish
from tests.unit.command.test_option_generation import generate_test_options_collection


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'unit'
ALL_VALID_OPTIONS['-s,--run-setup'] = [True, False]
ALL_VALID_OPTIONS['-t,--binary-expiration'] = 1000
ALL_VALID_OPTIONS['-f,--force-binary-build'] = [True, False]
ALL_VALID_OPTIONS['-m,--submit-binary'] = [True, False]
ALL_VALID_OPTIONS['-o,--disable-ota'] = [True, False]
ALL_VALID_OPTIONS['-b,--binary-build-process'] = 'turtle'
ALL_VALID_OPTIONS['-q,--qr-build-formats'] = 'formats'


@mock.patch('cot.command.run.expo_app_publish.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(run_expo_app_publish.params)
    runner = CliRunner()
    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_expo_app_publish, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
