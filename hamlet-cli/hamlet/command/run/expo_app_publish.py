import click
from hamlet.backend.run import expo_app_publish as run_expo_app_publish_backend
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options


@click.command(
    'expo-app-publish',
    short_help='Run a task based build of an Expo app binary',
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
@exceptions.backend_handler()
@pass_options
def expo_app_publish(options, **kwargs):
    """
    Run a task based build of an Expo app binary

    \b
    NOTES:
    RELEASE_CHANNEL default is environment
    """

    args = {
        **options.opts,
        **kwargs
    }

    run_expo_app_publish_backend.run(**args, _is_cli=True)
