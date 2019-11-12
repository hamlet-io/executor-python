from cot.command import root as cli
from .stack import stack
from .deployment import deployment
from .crypto import crypto
from .file_crypto import file_crypto


@cli.group('manage')
def group():
    """
    Manages stuff
    """


group.add_command(deployment)
group.add_command(stack)
group.add_command(crypto)
group.add_command(file_crypto)
