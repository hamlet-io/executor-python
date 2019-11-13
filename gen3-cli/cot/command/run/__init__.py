from cot.command import root as cli
from .expo_app_publish import expo_app_publish
from .task import task
from .lambda_func import lambda_func


@cli.group('run')
def group():
    """
    Runs stuff
    """


group.add_command(expo_app_publish)
group.add_command(task)
group.add_command(lambda_func)
