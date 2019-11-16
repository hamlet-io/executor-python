import os
import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.credentials_crypto import credentials_crypto as manage_credentials_crypto
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-n,--credential-path'] = 'credential_path'
ALL_VALID_OPTIONS['!-y,--credential-type'] = ['login', 'api', 'env']
ALL_VALID_OPTIONS['-e,--credential-email'] = 'email@email.com'
ALL_VALID_OPTIONS['-f,--crypto-file'] = 'crypto_file'
ALL_VALID_OPTIONS['-i,--credential-id'] = 'credential_id'
ALL_VALID_OPTIONS['-s,--credential-secret'] = 'credential_secret'
ALL_VALID_OPTIONS['-v,--visible'] = [True, False]


@mock.patch('cot.command.manage.credentials_crypto.subprocess')
def test_input_valid(subprocess_mock):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod('crypto_file')
        # testing that's impossible to run without full set of required options
        run_options_test(runner, manage_credentials_crypto, ALL_VALID_OPTIONS, subprocess_mock)


@mock.patch('cot.command.manage.credentials_crypto.subprocess')
def test_input_validation(subprocess_mock):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod('crypto_file')
        run_validatable_option_test(
            runner,
            manage_credentials_crypto,
            subprocess_mock,
            {
                '-n': 'credential_path',
                '-y': 'login'
            },
            [
                ('-y', 'invalidtype', 'login'),
                ('-f', 'nonexistingfile', 'crypto_file')
            ]
        )
