from hamlet.command import root as cli
from .cmdb import generate_tenant as generate_tenant_cmdb_cmd
from .cmdb import generate_account as generate_account_cmdb_cmd
from .cmdb import generate_product as generate_product_cmdb_cmd


@cli.group('generate')
def group():
    """
    Generates base CMDB file system structures
    """
    pass


group.add_command(generate_tenant_cmdb_cmd)
group.add_command(generate_account_cmdb_cmd)
group.add_command(generate_product_cmdb_cmd)
