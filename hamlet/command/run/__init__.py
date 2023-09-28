from hamlet.command import root as cli

from .expo_app_publish import expo_app_publish as expo_app_publish_cmd
from .sentry_release import sentry_release as sentry_release_cmd


@cli.group("run", context_settings=dict(max_content_width=240))
def group():
    """
    Runs stuff
    """


group.add_command(expo_app_publish_cmd)
group.add_command(sentry_release_cmd)
