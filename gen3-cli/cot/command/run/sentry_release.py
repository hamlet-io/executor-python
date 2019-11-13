import subprocess
import click
from cot import utils
from cot import env


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
def sentry_release(
    sentry_source_map_s3_url,
    sentry_url_prefix,
    sentry_release_name,
    run_setup
):
    """
    Upload sourcemap files to sentry for a specific release
    """
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'runSentryRelease.sh',
        options={
            '-m': sentry_source_map_s3_url,
            '-p': sentry_url_prefix,
            '-r': sentry_release_name,
            '-s': run_setup
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
