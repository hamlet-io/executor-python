import os
import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.manage.file_crypto import file_crypto as manage_file_crypto
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['-d,--decrypt'] = [True, False]
ALL_VALID_OPTIONS['-e,--encrypt'] = [True, False]
ALL_VALID_OPTIONS['-f,--crypto-file'] = 'crypto_file'
ALL_VALID_OPTIONS['-u,--update'] = [True, False]


@mock.patch('cot.command.manage.file_crypto.subprocess')
def test_input_valid(subprocess_mock):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod('crypto_file')
        run_options_test(runner, manage_file_crypto, ALL_VALID_OPTIONS, subprocess_mock)


@mock.patch('cot.command.manage.file_crypto.subprocess')
def test_input_validation(subprocess_mock):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod('crypto_file')
        run_validatable_option_test(
            runner,
            manage_file_crypto,
            subprocess_mock,
            {},
            [
                ('-f', 'nonexistingfile', 'crypto_file')
            ]
        )
