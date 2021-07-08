import collections
from unittest import mock
from click.testing import CliRunner

from hamlet.command.release import transfer_image as transfer_image

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

ALL_VALID_OPTIONS["!--source-account"] = "source_account"
ALL_VALID_OPTIONS["!--source-environment"] = "source_environment"


@mock.patch(
    "hamlet.command.release.transfer_image_backend.TransferImageAutomationRunner"
)
def test_input_valid(transfer_image_backend):
    run_options_test(
        CliRunner(), transfer_image, ALL_VALID_OPTIONS, transfer_image_backend
    )


@mock.patch(
    "hamlet.command.release.transfer_image_backend.TransferImageAutomationRunner"
)
def test_input_validation(transfer_image_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        transfer_image,
        transfer_image_backend,
        {
            "-u": "deployment_unit",
            "-r": "build_reference",
            "-f": "image_format",
            "--source-account": "source_account",
            "--source-environment": "source_environment",
        },
        [],
    )
