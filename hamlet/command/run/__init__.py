from hamlet.command import root as cli
from .expo_app_publish import expo_app_publish as expo_app_publish_cmd
from .task import task as task_cmd
from .lambda_func import lambda_func as lambda_func_cmd
from .pipeline import pipeline as pipeline_cmd
from .sentry_release import sentry_release as sentry_release_cmd


@cli.group('run')
def group():
    """
    Runs stuff
    """


group.add_command(expo_app_publish_cmd)
group.add_command(task_cmd)
group.add_command(lambda_func_cmd)
group.add_command(pipeline_cmd)
group.add_command(sentry_release_cmd)
