import click
import functools
import os

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config
from hamlet.command.common.display import json_or_table_option, wrap_text

from hamlet.backend.automation_tasks import upload_image as upload_image_backend
from hamlet.backend.automation_tasks import transfer_image as transfer_image_backend
from hamlet.backend.automation_tasks import update_build as update_build_backend
from hamlet.backend import query as query_backend


def query_imagedetails_output(options, query, query_params=None, sub_query_text=None):
    query_args = {
        **options.opts,
        "generation_entrance": "imagedetails",
        "output_filename": "imagedetails-config.json",
    }
    query_result = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=query,
        query_params=query_params,
        sub_query_text=sub_query_text,
        engine=options.engine
    )

    return query_result


def image_options(func):
    """Standard image details"""

    @click.option(
        "-u",
        "--deployment-unit",
        required=True,
        help="The deployment unit the image belongs to",
    )
    @click.option(
        "-r",
        "--build-reference",
        required=True,
        help="The unique reference for the build of this image - usually git commit",
    )
    @click.option(
        "--code-tag",
        help="A tag applied to your code repo which will be mapped to a build reference",
    )
    @click.option(
        "-f",
        "--image-format",
        help="The format of the code image",
        type=click.Choice(
            [
                "dataset",
                "rdssnapshot",
                "docker",
                "lambda",
                "lambda_jar",
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
        "-s",
        "--registry-scope",
        help="The scope of the registry to update the image to",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Image Detail handling
        """
        return func(*args, **kwargs)

    return wrapper


@cli.group("release", context_settings=dict(max_content_width=240))
def group():
    """
    Manage the lifecycle of images for occurrences
    """


@group.command(
    "upload-image", short_help="", context_settings=dict(max_content_width=240)
)
@image_options
@click.option(
    "--image-path",
    help="The path to the image can be zip file or directory",
    type=click.Path(file_okay=True, dir_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--dockerfile",
    help="The path to a dockerfile to create the image with",
    type=click.Path(file_okay=True, dir_okay=False, readable=True, resolve_path=True),
)
@click.option(
    "--docker-context",
    help="The docker context directory used with the dockerfile",
    type=click.Path(file_okay=False, dir_okay=True, readable=True, resolve_path=True),
)
@click.option("--docker-image", help="The tag of an existing docker image")
@exceptions.backend_handler()
@config.pass_options
def upload_image(options, **kwargs):
    """
    Upload a code image to a registry
    """
    task = upload_image_backend.UploadImageAutomationRunner(
        **options.opts, **kwargs, engine=options.engine
    )
    task.run()


@group.command(
    "transfer-image", short_help="", context_settings=dict(max_content_width=240)
)
@image_options
@click.option(
    "--source-account",
    required=True,
    help="The name of the account to get the image from",
)
@click.option(
    "--source-environment",
    required=True,
    help="The name of the environment to get the image from",
)
@exceptions.backend_handler()
@config.pass_options
def transfer_image(options, **kwargs):
    """
    Transfer an image between registries
    """
    task = transfer_image_backend.TransferImageAutomationRunner(
        **options.opts, **kwargs, engine=options.engine
    )
    task.run()


@group.command(
    "update-image-reference",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@image_options
@exceptions.backend_handler()
@config.pass_options
def update_image_reference(options, **kwargs):
    """
    Update the image reference for a component
    """
    task = update_build_backend.UpdateBuildAutomationRunner(
        **options.opts, **kwargs, engine=options.engine
    )
    task.run()


def image_references_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Occurrence"]),
                wrap_text(row["BUILD_UNIT"]),
                wrap_text(row["BUILD_REFERENCE"]),
                wrap_text(row["APP_REFERENCE"]),
                wrap_text(row["BUILD_FORMATS"]),
                wrap_text(row["BUILD_SOURCE"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=[
            "Occurrence",
            "Deployment Unit",
            "Build Reference",
            "Code Tag",
            "Image Format",
            "Image Source",
        ],
        tablefmt="github",
    )


@group.command(
    "list-image-references",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option("-q", "--query", help="A query to filter out the results")
@json_or_table_option(image_references_table)
@exceptions.backend_handler()
@config.pass_options
def list_image_references(options, query):
    """
    List the references for all components
    """

    LIST_IMAGE_REFERENCES_QUERY = (
        "Images[]"
        ".{"
        "Occurrence:Occurrence,"
        "BUILD_FORMATS:BUILD_FORMATS,"
        "BUILD_UNIT:BUILD_UNIT,"
        "BUILD_REFERENCE:BUILD_REFERENCE,"
        "APP_REFERENCE:APP_REFERENCE,"
        "BUILD_SOURCE:BUILD_SOURCE"
        "}"
    )

    return query_imagedetails_output(options, LIST_IMAGE_REFERENCES_QUERY, None, query)
