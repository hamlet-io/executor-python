import click

from cookiecutter.exceptions import OutputDirExistsException

from hamlet.backend.generate.cmdb import account as generate_account_backend
from hamlet.backend.generate.cmdb import tenant as generate_tenant_backend
from hamlet.backend.generate.cmdb import product as generate_product_backend
from hamlet.utils import dynamic_option, DynamicCommand
from hamlet.command.generate import decorators
from hamlet.command.common.exceptions import CommandError


@click.command(
    "tenant-cmdb", cls=DynamicCommand, context_settings=dict(max_content_width=240)
)
@dynamic_option(
    "--tenant-id",
    help="The unique Id for the tenant",
    prompt=True,
    prompt_required=True,
    required=True,
)
@dynamic_option(
    "--tenant-name",
    help="A more descriptive name for the tenant",
    default=lambda p: p.tenant_id,
)
@dynamic_option(
    "--default-region",
    help="The id of the default region to use for deployments in this tenant",
    default="ap-southeast-2",
)
@dynamic_option(
    "--audit-log-expiry-days",
    help="How long to keep account audit logs for",
    type=click.INT,
    default=2555,
)
@dynamic_option(
    "--audit-log-offline-days",
    help="How log until audit logs are sent to archive storage",
    type=click.INT,
    default=90,
)
@decorators.common_generate_options
def generate_tenant(**kwargs):
    """
    Creates a tenant cmdb.
    This should be run from the root of an accounts repository.
    """
    try:
        generate_tenant_backend.run(**kwargs)

    except OutputDirExistsException as e:
        raise CommandError(e)


@click.command(
    "account-cmdb", cls=DynamicCommand, context_settings=dict(max_content_width=240)
)
@dynamic_option(
    "--account-id",
    help="The unique id for the account",
    prompt=True,
    prompt_required=False,
    required=True,
)
@dynamic_option(
    "--account-name",
    help="A more descriptive name for the account",
    default=lambda p: p.account_id,
)
@dynamic_option(
    "--account-seed",
    help="A random seed to ensure unique deployments",
    default=lambda p: generate_account_backend.generate_account_seed(),
)
@dynamic_option(
    "--provider-type",
    help="The cloud provider the account represents",
    type=click.Choice(
        [
            "aws",
            "azure",
        ]
    ),
    default="aws",
)
@dynamic_option(
    "--provider-id",
    help="The cloud provider Id for for the account (AWS Account Id or Azure Subscription)",
    required=True,
    prompt=True,
    prompt_required=False,
)
@decorators.common_generate_options
def generate_account(**kwargs):
    """
    Creates an account cmdb within a tenant cmdb.

    The account template can be reused to create multiple accounts within a Tenant.
    This template should be run from a tenant directory
    """
    try:
        generate_account_backend.run(**kwargs)

    except OutputDirExistsException as e:
        raise CommandError(e)


@click.command(
    "product-cmdb", cls=DynamicCommand, context_settings=dict(max_content_width=240)
)
@dynamic_option(
    "--product-id",
    help="The Id of your product",
    prompt=True,
    prompt_required=False,
    required=True,
)
@dynamic_option(
    "--dns-zone",
    help="A DNS zone name which will act as a base domain for public component hostnames",
    default="",
)
@dynamic_option(
    "--product-name",
    help="A more descriptive name of your product",
    default=lambda p: p.product_id,
)
@dynamic_option(
    "--environment-id",
    help="The id of your first deployed environment",
    default="int",
)
@dynamic_option(
    "--environment-name",
    help="A more descriptive name of your environment",
    default="integration",
)
@dynamic_option(
    "--segment-id",
    help="The id of the first segment in your environments",
    default="default",
)
@dynamic_option(
    "--segment-name",
    help="A more descriptive name of your segment",
    default=lambda p: p.segment_id,
)
@decorators.common_generate_options
def generate_product(**kwargs):
    """
    Creates a product cmdb.
    This template should be run from the root of an empty product directory.
    """
    try:
        generate_product_backend.run(**kwargs)
    except OutputDirExistsException as e:
        raise CommandError(e)
