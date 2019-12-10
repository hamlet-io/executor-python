from unittest import mock
from click.testing import CliRunner
from cot.command.generate.cmdb import generate_tenant
from tests.unit.command.generate.utils import inputlines


@mock.patch('cot.command.generate.cmdb.generate_tenant_backend')
def test(generate_tenant_backend):
    runner = CliRunner()
    result = runner.invoke(
        generate_tenant,
        [
            '--tenant-id',
            'tenant-id'
        ]
    )
    assert result.exit_code == 0, result.output
    assert generate_tenant_backend.run.call_count == 1

    generate_tenant_backend.run.assert_called_once_with(
        tenant_id='tenant-id',
        tenant_name='tenant-id',
        domain_stem='',
        default_region='ap-southeast-2',
        audit_log_expiry_days=2555,
        audit_log_offline_days=90
    )

    generate_tenant_backend.reset_mock()
    result = runner.invoke(
        generate_tenant,
        [
            '--tenant-id',
            'id',

            '--tenant-name',
            'name',

            '--domain-stem',
            'domain.stem.com',

            '--default-region',
            'ap-southwest-1',

            '--audit-log-expiry-days',
            '10',

            '--audit-log-offline-days',
            '11'
        ]
    )
    assert result.exit_code == 0, result.output
    generate_tenant_backend.run.assert_called_once_with(
        tenant_id='id',
        tenant_name='name',
        domain_stem='domain.stem.com',
        default_region='ap-southwest-1',
        audit_log_expiry_days=10,
        audit_log_offline_days=11
    )

    generate_tenant_backend.reset_mock()
    result = runner.invoke(
        generate_tenant,
        [
            '--prompt'
        ],
        input=inputlines(
            'id',
            'name',
            'domain.stem.com',
            'ap-southwest-1',
            '10',
            '11',
            'y'
        )
    )
    assert result.exit_code == 0, result.output
    generate_tenant_backend.run.assert_called_once_with(
        tenant_id='id',
        tenant_name='name',
        domain_stem='domain.stem.com',
        default_region='ap-southwest-1',
        audit_log_expiry_days=10,
        audit_log_offline_days=11
    )

    generate_tenant_backend.reset_mock()
    result = runner.invoke(
        generate_tenant,
        [
            '--prompt',
            '--use-default'
        ],
        input=inputlines(
            'tenant-id',
            'y'
        )
    )
    assert result.exit_code == 0, result.output
    generate_tenant_backend.run.assert_called_once_with(
        tenant_id='tenant-id',
        tenant_name='tenant-id',
        domain_stem='',
        default_region='ap-southeast-2',
        audit_log_expiry_days=2555,
        audit_log_offline_days=90
    )
