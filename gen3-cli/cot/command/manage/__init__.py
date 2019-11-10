from cot.command import root as cli
from .stack import stack
from .deployment import deployment


@cli.group('manage')
def group():
    """
    Manages stuff
    """

group.add_command(deployment)
group.add_command(stack)
