import os
import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.credentials_crypto import credentials_crypto as manage_credentials_crypto
from tests.unit.command.test_option_generation import generate_test_options_collection


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
    assert len(ALL_VALID_OPTIONS) == len(manage_credentials_crypto.params)
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod('crypto_file')
        for args in generate_test_options_collection(ALL_VALID_OPTIONS):
            result = runner.invoke(manage_credentials_crypto, args)
            assert result.exit_code == 0, result.output
            assert subprocess_mock.run.call_count == 1
            subprocess_mock.run.call_count = 0
