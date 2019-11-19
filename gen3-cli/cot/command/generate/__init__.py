from cot.command import root as cli
from .cmdb import group as cmdb_generation_group
from .product import group as product_generation_group


@cli.group('generate')
def group():
    """
    Generate various cmdb components
    """
    pass


group.add_command(cmdb_generation_group)
group.add_command(product_generation_group)
