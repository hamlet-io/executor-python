import subprocess
from cot import utils
from cot import env


def run(
    sentry_source_map_s3_url=None,
    sentry_url_prefix=None,
    sentry_release_name=None,
    run_setup=None
):
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
