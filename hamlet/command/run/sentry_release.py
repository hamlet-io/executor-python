import click
from hamlet.backend.run import sentry_release as run_sentry_release_backend
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options


@click.command(
    "sentry-release",
    short_help="Upload sourcemap files to sentry for a specific release",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "-m", "--sentry-source-map-s3-url", required=True, help="s3 link to sourcemap files"
)
@click.option("-p", "--sentry-url-prefix", help="prefix for sourcemap files")
@click.option("-r", "--sentry-release-name", help="sentry release name", required=True)
@click.option(
    "-s", "--run-setup", help="run setup installation to prepare", is_flag=True
)
@exceptions.backend_handler()
@pass_options
def sentry_release(options, **kwargs):
    """
    Upload sourcemap files to sentry for a specific release
    """

    args = {**options.opts, **kwargs}

    run_sentry_release_backend.run(**args, _is_cli=True)
