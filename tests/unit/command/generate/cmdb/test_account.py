import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.generate.cmdb import generate_account
from tests.unit.command.generate.test_generate_command import run_generate_command_test

OPTIONS = collections.OrderedDict()
OPTIONS["!--account-id,account_id"] = "test-account-id"
OPTIONS["!--provider-id,provider_id"] = "test-provider-id"
OPTIONS["--account-name,account_name"] = ("test-account-name", "test-account-id")
OPTIONS["--account-seed,account_seed"] = ("not-random-seed", "random-seed")
OPTIONS["--provider-type,provider_type"] = ("aws", "azure")


@mock.patch("hamlet.command.generate.cmdb.generate_account_backend")
def test(generate_account_backend):
    generate_account_backend.generate_account_seed.return_value = "random-seed"
    run_generate_command_test(
        CliRunner(), generate_account, generate_account_backend.run, OPTIONS
    )
