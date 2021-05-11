from hamlet.command import root as cli

from .create import create_deployments as create_deployments_cmd
from .list import list_deployments as list_deployments_cmd
from .run import run_deployments as run_deployments_cmd
from .test import test_deployments as test_deployments_cmd


@cli.group('deploy')
def group():
    """
    Deploys infrastructure based on the hamlet cmdb
    """
    pass


group.add_command(create_deployments_cmd)
group.add_command(list_deployments_cmd)
group.add_command(run_deployments_cmd)
group.add_command(test_deployments_cmd)
