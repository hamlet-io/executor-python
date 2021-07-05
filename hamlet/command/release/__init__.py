import click

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config

from hamlet.backend.automation_tasks import upload_image as upload_image_backend
from hamlet.backend.automation_tasks import transfer_image as transfer_image_backend
from hamlet.backend.automation_tasks import update_build as update_build_backend


@cli.group("release")
def group():
    """
    Manage the lifecycle of code images
    """


@group.command(
    "upload-image", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "--deployment-unit",
    envvar="DEPLOYMENT_UNIT",
    required=True,
    help="The deployment unit the code belongs to",
)
@click.option(
    "--build-reference",
    envvar="BUILD_REFERENCE",
    required=True,
    help="The unique reference for the build of this image - usually git commit",
)
@click.option(
    "--image-format",
    envvar="IMAGE_FORMAT",
    required=True,
    help="The format of the code image",
    type=click.Choice(
        [
            "dataset",
            "rdssnapshot",
            "docker",
            "lambda",
            "pipeline",
            "scripts",
            "openapi",
            "swagger",
            "spa",
            "contentnode",
        ]
    ),
)
@click.option(
    "--image-path",
    envvar="IMAGE_PATH",
    help="The path to the image can be zip file or directory",
    type=click.Path(file_okay=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--dockerfile",
    envvar="DOCKERFILE",
    help="The path to a dockerfile to create the image with",
    type=click.Path(file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
@click.option(
    "--docker-context",
    envvar="DOCKER_CONTEXT",
    help="The docker context directory used with the dockerfile",
    type=click.Path(file_okay=False, dir_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--docker-image", envvar="DOCKER_IMAGE", help="The tag of an existing docker image"
)
@click.option(
    "--registry-scope",
    envvar="REGISTRY_SCOPE",
    help="The scope of the registry to update the image to",
)
@exceptions.backend_handler()
@config.pass_options
def upload_image(opts, **kwargs):
    """
    Upload a code image to a registry
    """
    task = upload_image_backend.UploadImageAutomationRunner(**opts.opts, **kwargs)
    task.run()


@group.command(
    "transfer-image", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "--source-account",
    envvar="SOURCE_ACCOUNT",
    required=True,
    help="The Id of the account to get the release from",
)
@click.option(
    "--source-environment",
    envvar="SOURCE_ENVIRONMENT",
    required=True,
    help="The Id of the environment to get the release from",
)
@click.option(
    "--deployment-unit",
    envvar="DEPLOYMENT_UNITS",
    required=True,
    multiple=True,
    help="A list of deployment unit releases to transfer - uses all if not set",
)
@click.option(
    "--build-reference",
    envvar="BUILD_REFERENCE",
    required=True,
    help="The unique reference of the image you want to transfer - usually git full hash",
)
@click.option(
    "--image-format",
    envvar="IMAGE_FORMAT",
    required=True,
    help="The format of the code image",
    type=click.Choice(
        [
            "dataset",
            "rdssnapshot",
            "docker",
            "lambda",
            "pipeline",
            "scripts",
            "openapi",
            "swagger",
            "spa",
            "contentnode",
        ]
    ),
)
@exceptions.backend_handler()
@config.pass_options
def transfer_image(opts, **kwargs):
    """
    Transfer an image between registries
    """
    task = transfer_image_backend.TransferImageAutomationRunner(**opts.opts, **kwargs)
    task.run()


@group.command(
    "update-image-reference",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "--deployment-unit",
    envvar="DEPLOYMENT_UNIT",
    required=True,
    help="The deployment unit the code belongs to",
)
@click.option(
    "--build-reference",
    envvar="BUILD_REFERENCE",
    required=True,
    help="The unique reference for the build of this image - usually git commit",
)
@click.option(
    "--code-tag",
    envvar="CODE_TAG",
    help="A tag applied to your code repo which will be mapped to a build reference",
)
@click.option(
    "--image-format",
    envvar="IMAGE_FORMAT",
    required=True,
    help="The format of the code image",
    type=click.Choice(
        [
            "dataset",
            "rdssnapshot",
            "docker",
            "lambda",
            "pipeline",
            "scripts",
            "openapi",
            "swagger",
            "spa",
            "contentnode",
        ]
    ),
)
@click.option(
    "--registry-scope",
    envvar="REGISTRY_SCOPE",
    help="The scope of the registry to update the image to",
)
@exceptions.backend_handler()
@config.pass_options
def update_image_reference(opts, **kwargs):
    """
    Update the image reference for a component
    """
    task = update_build_backend.UpdateBuildAutomationRunner(**opts.opts, **kwargs)
    task.run()
