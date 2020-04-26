import click
from hamlet.backend.run import sentry_release as run_sentry_release_backend


@click.command(
    'sentry-release',
    short_help='Upload sourcemap files to sentry for a specific release',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-m',
    '--sentry-source-map-s3-url',
    required=True,
    help='s3 link to sourcemap files'
)
@click.option(
    '-p',
    '--sentry-url-prefix',
    help='prefix for sourcemap files'
)
@click.option(
    '-r',
    '--sentry-release-name',
    help='sentry release name',
    required=True
)
@click.option(
    '-s',
    '--run-setup',
    help='run setup installation to prepare',
    is_flag=True
)
def sentry_release(**kwargs):
    """
    Upload sourcemap files to sentry for a specific release
    """
    run_sentry_release_backend.run(**kwargs, _is_cli=True)
