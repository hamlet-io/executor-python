import collections
from unittest import mock
from click.testing import CliRunner

from hamlet.command.release import update_image_reference as update_image_reference

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


@mock.patch("hamlet.command.release.update_build_backend.UpdateBuildAutomationRunner")
def test_input_valid(update_image_reference_backend):
    run_options_test(
        CliRunner(),
        update_image_reference,
        ALL_VALID_OPTIONS,
        update_image_reference_backend,
    )


@mock.patch("hamlet.command.release.update_build_backend.UpdateBuildAutomationRunner")
def test_input_validation(update_image_reference_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        update_image_reference,
        update_image_reference_backend,
        {
            "-u": "deployment_unit",
            "-r": "build_reference",
            "-f": "image_format",
        },
        [],
    )
