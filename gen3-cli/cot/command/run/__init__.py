from cot.command import root as cli
from .expo_app_publish import expo_app_publish
from .task import task
from .lambda_func import lambda_func
from .pipeline import pipeline
from .sentry_release import sentry_release


@cli.group('run')
def group():
    """
    Runs stuff
    """


group.add_command(expo_app_publish)
group.add_command(task)
group.add_command(lambda_func)
group.add_command(pipeline)
group.add_command(sentry_release)
