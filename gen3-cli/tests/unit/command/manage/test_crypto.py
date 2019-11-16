import os
import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.crypto import crypto as manage_crypto
from tests.unit.command.test_option_generation import generate_test_options_collection


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['-a,--alias'] = 'alias'
ALL_VALID_OPTIONS['-b,--base64-decode'] = [True, False]
ALL_VALID_OPTIONS['-d,--decrypt'] = [True, False]
ALL_VALID_OPTIONS['-e,--encrypt'] = [True, False]
ALL_VALID_OPTIONS['-f,--crypto-file'] = 'crypto_file'
ALL_VALID_OPTIONS['-k,--key-id'] = 'key_id'
ALL_VALID_OPTIONS['-n,--no-alteration'] = [True, False]
ALL_VALID_OPTIONS['-p,--json-path'] = 'path.inside.json.file'
ALL_VALID_OPTIONS['-q,--quiet'] = [True, False]
ALL_VALID_OPTIONS['-t,--crypto-text'] = 'ciphertext'
ALL_VALID_OPTIONS['-u,--update'] = [True, False]
ALL_VALID_OPTIONS['-v,--visible'] = [True, False]


@mock.patch('cot.command.manage.crypto.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(manage_crypto.params)
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod('crypto_file')
        for args in generate_test_options_collection(ALL_VALID_OPTIONS):
            result = runner.invoke(manage_crypto, args)
            assert result.exit_code == 0, result.output
            assert subprocess_mock.run.call_count == 1
            subprocess_mock.run.call_count = 0


@mock.patch('cot.command.manage.crypto.subprocess')
def test_input_validation(subprocess_mock):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # testing crypto-file option
        result = runner.invoke(
            manage_crypto,
            [
                '-f', 'crypto_file'
            ]
        )
        assert result.exit_code == 2, result.output
        assert subprocess_mock.run.call_count == 0
        # creating file
        os.mknod('crypto_file')
        result = runner.invoke(
            manage_crypto,
            [
                '-f', 'crypto_file'
            ]
        )
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
