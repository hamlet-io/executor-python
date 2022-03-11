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
    "-u",
    "--deployment-unit",
    required=True,
    help="mobile app deployment unit",
    envvar="DEPLOYMENT_UNIT",
)
@click.option(
    "-s",
    "--run-setup",
    is_flag=True,
    help="run setup installation to prepare",
    envvar="RUN_SETUP",
)
@click.option(
    "-f",
    "--force-binary-build",
    help="force the build of binary images",
    is_flag=True,
    envvar="FORCE_BINARY_BUILD",
)
@click.option(
    "-m",
    "--submit-binary",
    help="submit the binary for testing",
    is_flag=True,
    envvar="SUBMIT_BINARY",
)
@click.option(
    "-b",
    "--binary-build-process",
    help="sets the build process to create the binary",
    type=click.Choice(["fastlane", "turtle"]),
    envvar="BINARY_BUILD_PROCESS",
)
@click.option(
    "-l",
    "--build-logs",
    help="Show the full build logs",
    is_flag=True,
    envvar="BUILD_LOGS",
)
@click.option(
    "-e",
    "--environment-badge",
    help="Add a badge to the app icons for the environment",
    is_flag=True,
    envvar="ENVIRONMENT_BADGE",
)
@click.option(
    "-d",
    "--environment-badge-content",
    help="An override to the environment badge content",
    envvar="ENVIRONMENT_BADGE_CONTENT",
)
@click.option(
    "-n",
    "--node-package-manager",
    help="The node package manager to use for builds",
    type=click.Choice(["yarn", "npm"]),
    envvar="NODE_PACKAGE_MANAGER",
)
@click.option(
    "-o",
    "--binary-output-dir",
    type=click.Path(dir_okay=True, file_okay=False, writable=True, resolve_path=True),
    help="The directory to save generated binaries to",
)
@click.option(
    "-v",
    "--app-version-source",
    help="The method to use to source the app version",
    type=click.Choice(["cmdb", "manifest"]),
    envvar="APP_VERSION_SOURCE",
)
@exceptions.backend_handler()
@pass_options
def expo_app_publish(options, **kwargs):
    """
    Run a task based build of an Expo app binary
    """

    args = {**options.opts, **kwargs}
    run_expo_app_publish_backend.run(**args, engine=options.engine, _is_cli=True)
