import collections
from unittest import mock
from click.testing import CliRunner

from hamlet.command.release import upload_image as upload_image

from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS["!-u,--deployment-unit"] = "deployment_unit"
ALL_VALID_OPTIONS["!-r,--build-reference"] = "build_reference"
ALL_VALID_OPTIONS["--code-tag"] = "code_tag"
ALL_VALID_OPTIONS["-f,--image-format"] = "docker"
ALL_VALID_OPTIONS["-s,--registry-scope"] = "registry_scope"

ALL_VALID_OPTIONS["--image-path"] = "image_path"
ALL_VALID_OPTIONS["--dockerfile"] = "dockerfile"
ALL_VALID_OPTIONS["--docker-context"] = "docker_context"
ALL_VALID_OPTIONS["--docker-image"] = "docker_image"


@mock.patch("hamlet.command.release.upload_image_backend.UploadImageAutomationRunner")
def test_input_valid(upload_image_backend):
    run_options_test(CliRunner(), upload_image, ALL_VALID_OPTIONS, upload_image_backend)


@mock.patch("hamlet.command.release.upload_image_backend.UploadImageAutomationRunner")
def test_input_validation(upload_image_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        upload_image,
        upload_image_backend,
        {
            "-u": "deployment_unit",
            "-r": "build_reference",
            "-f": "image_format",
        },
        [],
    )
