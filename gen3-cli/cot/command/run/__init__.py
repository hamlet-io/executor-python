from cot.command import root as cli
from .expo_app_publish import expo_app_publish


@cli.group('run')
def group():
    """
    Runs stuff
    """


group.add_command(expo_app_publish)
