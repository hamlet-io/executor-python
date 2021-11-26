import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.manage.crypto import crypto as manage_crypto
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["-a,--alias"] = "alias"
ALL_VALID_OPTIONS["-b,--base64-decode"] = [True, False]
ALL_VALID_OPTIONS["-d,--decrypt"] = [True, False]
ALL_VALID_OPTIONS["-e,--encrypt"] = [True, False]
ALL_VALID_OPTIONS["-f,--crypto-file"] = "crypto_file"
ALL_VALID_OPTIONS["-k,--key-id"] = "key_id"
ALL_VALID_OPTIONS["-n,--no-alteration"] = [True, False]
ALL_VALID_OPTIONS["-p,--json-path"] = "path.inside.json.file"
ALL_VALID_OPTIONS["-q,--quiet"] = [True, False]
ALL_VALID_OPTIONS["-t,--crypto-text"] = "ciphertext"
ALL_VALID_OPTIONS["-u,--update"] = [True, False]
ALL_VALID_OPTIONS["-v,--visible"] = [True, False]


@mock.patch("hamlet.command.manage.crypto.manage_crypto_backend")
def test_input_valid(manage_crypto_backend):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("crypto_file", "w").close()
        run_options_test(
            runner, manage_crypto, ALL_VALID_OPTIONS, manage_crypto_backend.run
        )


@mock.patch("hamlet.command.manage.crypto.manage_crypto_backend")
def test_input_validation(manage_crypto_backend):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("crypto_file", "w").close()
        run_validatable_option_test(
            runner,
            manage_crypto,
            manage_crypto_backend.run,
            {},
            [("-f", "nonexistingfile", "crypto_file")],
        )
