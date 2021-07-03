import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.generate.cmdb import generate_tenant
from tests.unit.command.generate.test_generate_command import run_generate_command_test

OPTIONS = collections.OrderedDict()
OPTIONS["!--tenant-id,tenant_id"] = "test-tenant-id"
OPTIONS["--tenant-name,tenant_name"] = ("test-tenant-name", "test-tenant-id")
OPTIONS["--default-region,default_region"] = ("ap-southwest-1", "ap-southeast-2")
OPTIONS["--audit-log-expiry-days,audit_log_expiry_days"] = (10, 2555)
OPTIONS["--audit-log-offline-days,audit_log_offline_days"] = (11, 90)


@mock.patch("hamlet.command.generate.cmdb.generate_tenant_backend")
def test(generate_tenant_backend):
    run_generate_command_test(
        CliRunner(), generate_tenant, generate_tenant_backend.run, OPTIONS
    )
