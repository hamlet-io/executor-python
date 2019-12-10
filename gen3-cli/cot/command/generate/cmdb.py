import click
from cot.backend.generate.cmdb import account as generate_account_backend
from cot.backend.generate.cmdb import tenant as generate_tenant_backend
from cot.utils import dynamic_option
from cot.command.generate import utils


@click.group('cmdb')
def group():  # pragma: no cover
    pass


@group.command('account')
@dynamic_option('--account-id', required=True)
@dynamic_option('--account-name', default=lambda p: p.account_id)
@dynamic_option('--account-seed', default=lambda p: generate_account_backend.generate_account_seed())
@dynamic_option('--account-type', default='aws')
@dynamic_option('--aws-account-id', default=lambda p: '' if p.account_type == 'aws' else 'n/a')
@click.option('--prompt', is_flag=True)
@click.option('--use-default', is_flag=True)
@click.pass_context
def generate_account(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of a codeontap account.
    The account template can be reused to create multiple accounts within a Tenant.

    This template should be run from a tenant directory
    """
    if not prompt or utils.confirm(kwargs):
        generate_account_backend.run(**kwargs)


@group.command('tenant')
@dynamic_option('--tenant-id', required=True)
@dynamic_option('--tenant-name', default=lambda p: p.tenant_id)
@dynamic_option('--domain-stem', default='')
@dynamic_option('--default-region', default='ap-southeast-2')
@dynamic_option('--audit-log-expiry-days', type=click.INT, default=2555)
@dynamic_option('--audit-log-offline-days', type=click.INT, default=90)
@click.option('--prompt', is_flag=True)
@click.option('--use-default', is_flag=True)
@click.pass_context
def generate_tenant(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of a codeontap tenant.
    This should be run from the root of an accounts repository.
    """
    if not prompt or utils.confirm(kwargs):
        generate_tenant_backend.run(**kwargs)
