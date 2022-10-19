import click
from hamlet.backend.run import sentry_release as run_sentry_release_backend
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options


@click.command(
    "sentry-release",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "-u",
    "--deployment-unit",
    required=True,
    help="The deployment unit of the moobile app",
)
@click.option(
    "-g",
    "--deployment-group",
    default="application",
    help="The deployment group of the moobile app",
)
@click.option(
    "-m", "--sentry-source-map-s3-url", required=True, help="s3 link to sourcemap files"
)
@click.option(
    "-a",
    "--app-type",
    type=click.Choice(["", "react-native"]),
    help="The application framework being used",
)
@click.option(
    "-d",
    "--dist",
    help="A distribution Identifier for the file",
)
@click.option("-p", "--sentry-url-prefix", help="prefix for sourcemap files")
@click.option(
    "-r",
    "--sentry-release-name",
    help="release name",
    required=True,
)
@exceptions.backend_handler()
@pass_options
def sentry_release(options, **kwargs):
    """
    Upload sourcemap files to sentry for a specific release
    """

    args = {**options.opts, **kwargs}
    run_sentry_release_backend.run(**args, engine=options.engine, _is_cli=True)
