from cot.command import root as cli
from .stack import stack


@cli.group('manage')
def group():
    """
    Manages stuff
    """


group.add_command(stack)
