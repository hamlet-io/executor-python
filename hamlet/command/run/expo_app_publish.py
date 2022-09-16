import click
from hamlet.backend.run import expo_app_publish as run_expo_app_publish_backend
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options


@click.command(
    "expo-app-publish",
    short_help="Run a task based build of an Expo app binary",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "-l",
    "--deployment-group",
    help="mobile app deployment group",
    default="application",
    envvar="DEPLOYMENT_GROUP",
)
@click.option(
    "-u",
    "--deployment-unit",
    required=True,
    help="mobile app deployment unit",
    envvar="DEPLOYMENT_UNIT",
)
@click.option(
    "-n",
    "--node-package-manager",
    help="The node package manager to use for builds",
    type=click.Choice(["auto", "yarn", "npm"]),
    envvar="NODE_PACKAGE_MANAGER",
)
@click.option(
    "-o",
    "--binary-output-dir",
    type=click.Path(dir_okay=True, file_okay=False, writable=True, resolve_path=True),
    help="The directory to save generated binaries to",
)
@exceptions.backend_handler()
@pass_options
def expo_app_publish(options, **kwargs):
    """
    Run a task based build of an Expo app binary
    """

    args = {**options.opts, **kwargs}
    run_expo_app_publish_backend.run(
        **args,
        build_logs=(options.opts.get("log_level", "info") in ["debug", "trace"]),
        engine=options.engine,
        _is_cli=True
    )
