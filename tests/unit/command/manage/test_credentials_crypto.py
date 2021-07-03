import os
import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.manage.credentials_crypto import (
    credentials_crypto as manage_credentials_crypto,
)
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-n,--credential-path"] = "credential_path"
ALL_VALID_OPTIONS["!-y,--credential-type"] = ["login", "api", "env"]
ALL_VALID_OPTIONS["-e,--credential-email"] = "email@email.com"
ALL_VALID_OPTIONS["-f,--crypto-file"] = "crypto_file"
ALL_VALID_OPTIONS["-i,--credential-id"] = "credential_id"
ALL_VALID_OPTIONS["-s,--credential-secret"] = "credential_secret"
ALL_VALID_OPTIONS["-v,--visible"] = [True, False]


@mock.patch(
    "hamlet.command.manage.credentials_crypto.manage_credentials_crypto_backend"
)
def test_input_valid(manage_credentials_crypto_backend):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod("crypto_file")
        # testing that's impossible to run without full set of required options
        run_options_test(
            runner,
            manage_credentials_crypto,
            ALL_VALID_OPTIONS,
            manage_credentials_crypto_backend.run,
        )


@mock.patch(
    "hamlet.command.manage.credentials_crypto.manage_credentials_crypto_backend"
)
def test_input_validation(manage_credentials_crypto_backend):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mknod("crypto_file")
        run_validatable_option_test(
            runner,
            manage_credentials_crypto,
            manage_credentials_crypto_backend.run,
            {"-n": "credential_path", "-y": "login"},
            [("-y", "invalidtype", "login"), ("-f", "nonexistingfile", "crypto_file")],
        )
