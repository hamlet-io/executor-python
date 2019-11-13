import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'expo-app-publish',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-u',
    '--deployment-unit',
    required=True,
    help='mobile app deployment unit'
)
@click.option(
    '-s',
    '--run-setup',
    is_flag=True,
    help='run setup installation to prepare'
)
@click.option(
    '-t',
    '--binary-expiration',
    help='how long presigned urls are active for once created ( seconds )',
    type=click.INT,
    default=1210000,
    show_default=True
)
@click.option(
    '-f',
    '--force-binary-build',
    help='force the build of binary images',
    is_flag=True
)
@click.option(
    '-m',
    '--submit-binary',
    help='submit the binary for testing',
    is_flag=True
)
@click.option(
    '-o',
    '--disable-ota',
    help="don't publish the OTA to the CDN",
    is_flag=True
)
@click.option(
    '-b',
    '--binary-build-process',
    help='sets the build process to create the binary',
    default='turtle',
    show_default=True
)
@click.option(
    '-q',
    '--qr-build-formats',
    help='formats you would like to generate QR urls for',
    default='ios,android',
    show_default=True
)
def expo_app_publish(
    deployment_unit,
    run_setup,
    binary_expiration,
    force_binary_build,
    submit_binary,
    disable_ota,
    binary_build_process,
    qr_build_formats
):
    """
    Run a task based build of an Expo app binary

    \b
    NOTES:
    RELEASE_CHANNEL default is environment
    """
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'runExpoAppPublish.sh',
        options={
            '-u': deployment_unit,
            '-s': run_setup,
            '-t': binary_expiration,
            '-f': force_binary_build,
            '-m': submit_binary,
            '-o': disable_ota,
            '-b': binary_build_process,
            '-q': qr_build_formats
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
