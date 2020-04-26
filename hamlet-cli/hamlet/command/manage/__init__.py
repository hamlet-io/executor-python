from hamlet.command import root as cli
from .stack import stack as stack_cmd
from .deployment import deployment as deployment_cmd
from .crypto import crypto as crypto_cmd
from .file_crypto import file_crypto as file_crypto_cmd
from .credentials_crypto import credentials_crypto as credentials_crypto_cmd


@cli.group('manage')
def group():
    """
    Manages stuff
    """


group.add_command(deployment_cmd)
group.add_command(stack_cmd)
group.add_command(crypto_cmd)
group.add_command(file_crypto_cmd)
group.add_command(credentials_crypto_cmd)
