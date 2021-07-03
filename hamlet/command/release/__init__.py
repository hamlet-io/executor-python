from os import environ
import click

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config
from hamlet.backend.automation_tasks import (
    accept_release,
    manage_images,
    transfer_release,
    update_build
)

@cli.group('release')
def group():
    '''
    Manage the lifecycle of code images
    '''


@group.command(
    'upload-image',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '--deployment-unit',
    envvar='DEPLOYMENT_UNIT',
    required=True,
    help='The deployment unit the code belongs to'
)
@click.option(
    '--build-reference',
    envvar='BUILD_REFERENCE',
    required=True,
    help='The unique reference for the build of this image - usually git commit'
)
@click.option(
    '--image-format',
    envvar='IMAGE_FORMAT',
    required=True,
    help='The format of the code image',
    type=click.Choice(
        [
            'dataset',
            'rdssnapshot',
            'docker',
            'lambda',
            'pipeline',
            'scripts',
            'openapi',
            'swagger',
            'spa',
            'contentnode'
        ]
    )
)
@click.option(
    '--image-path',
    envvar='IMAGE_PATH',
    help='The path to the image can be zip file or directory',
    type=click.Path(
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True
    )
)
@click.option(
    '--dockerfile',
    envvar='DOCKERFILE',
    help='The path to a dockerfile to create the image with',
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True
    )
)
@click.option(
    '--docker-context',
    envvar='DOCKER_CONTEXT',
    help='The docker context directory used with the dockerfile',
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True
    )
)
@click.option(
    '--docker-image',
    envvar='DOCKER_IMAGE',
    help='The tag of an existing docker image'
)
@click.option(
    '--registry-scope',
    envvar='REGISTRY_SCOPE',
    help='The scope of the registry to update the image to'
)
@exceptions.backend_handler()
@config.pass_options
def upload_image(opts, **kwargs):
    '''
    Upload a code image to a registry
    '''
    task = manage_images.ManageImagesAutomationRunner(
        { **kwargs, **opts.opts }
    )
    task.run()


@group.command(
    'update-build-reference',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@exceptions.backend_handler()
@config.pass_options
def update_build_reference(opts):
    '''
    Update the build reference for a component
    '''
    pass


@group.command(
    'transfer-environment-release',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@exceptions.backend_handler()
@config.pass_options
def transfer_environment_release(opts):
    '''
    Transfer a release between environments
    '''
    pass


@group.command(
    'accept-environment-release',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@exceptions.backend_handler()
@config.pass_options
def transfer_environment_release(opts):
    '''
    Accept a release into an environment
    '''
    pass
