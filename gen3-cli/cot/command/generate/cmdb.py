import os
from cookiecutter.main import cookiecutter
import click
from cot import conf


TEMPLATES_DIR = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, 'cmdb')


@click.group('cmdb')
def group():
    pass


@group.command('account')
def generate_account():
    """
    This template is for the creation of a codeontap account.
    The account template can be reused to create multiple accounts within a Tenant.

    This template should be run from a tenant directory
    """
    template_path = os.path.join(TEMPLATES_DIR, 'account')
    cookiecutter(template_path)


@group.command('tenant')
def generate_tenant():
    """
    This template is for the creation of a codeontap tenant.
    This should be run from the root of an accounts repository.
    """
    template_path = os.path.join(TEMPLATES_DIR, 'tenant')
    cookiecutter(template_path)
