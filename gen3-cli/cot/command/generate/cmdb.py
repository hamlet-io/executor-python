import click
from cot import utils
from cot.backend.generate.cmdb import account as generate_account_backend
from cot.backend.generate.cmdb import tenant as generate_tenant_backend


@click.group('cmdb')
def group():
    pass


@group.command('account')
@click.option(
    '--id'
)
@click.option(
    '--name'
)
@click.option(
    '--seed'
)
@click.option(
    '--type'
)
@click.option(
    '--aws-account-id'
)
@click.option(
    '--use-default',
    is_flag=True
)
@click.option(
    '--prompt',
    is_flag=True
)
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
    if not prompt:
        generate_account_backend.run(**kwargs)
        return
    prompt = utils.ClickMissingOptionsPrompt(ctx, kwargs, use_default)
    prompt.id()
    prompt.name(default=kwargs['id'])
    prompt.type(default='aws')
    prompt.seed(default=generate_account_backend.generate_account_seed())
    prompt.aws_account_id()

    if prompt.confirm():
        generate_account_backend.run(**kwargs)


@group.command('tenant')
@click.option(
    '-i',
    '--id'
)
@click.option(
    '-n',
    '--name'
)
@click.option(
    '-d',
    '--domain-stem'
)
@click.option(
    '-r',
    '--default-region'
)
@click.option(
    '-a',
    '--audit-log-expiry-days',
    type=click.INT
)
@click.option(
    '-o',
    '--audit-log-offline-days',
    type=click.INT
)
@click.option(
    '-d',
    '--use-default',
    is_flag=True
)
@click.option(
    '--prompt',
    is_flag=True
)
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
    if not prompt:
        generate_tenant_backend.run(**kwargs)
        return
    prompt = utils.ClickMissingOptionsPrompt(ctx, kwargs, use_default)
    prompt.id()
    prompt.name(default=kwargs['id'])
    prompt.domain_stem()
    prompt.default_region(default='ap-southeast-2')
    prompt.audit_log_expiry_days(default=2555)
    prompt.audit_log_offline_days(default=2555)

    if prompt.confirm():
        generate_tenant_backend.run(**kwargs)
