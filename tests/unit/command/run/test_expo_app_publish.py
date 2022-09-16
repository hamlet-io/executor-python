import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.run.expo_app_publish import expo_app_publish as run_expo_app_publish
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["-l,--deployment-group"] = "group"
ALL_VALID_OPTIONS["!-u,--deployment-unit"] = "unit"
ALL_VALID_OPTIONS["-n,--node-package-manager"] = "auto"
ALL_VALID_OPTIONS["-o,--binary-output-dir"] = "binary_output_dir"


@mock.patch("hamlet.command.run.expo_app_publish.run_expo_app_publish_backend")
def test_input_valid(run_expo_app_publish_backend):
    run_options_test(
        CliRunner(),
        run_expo_app_publish,
        ALL_VALID_OPTIONS,
        run_expo_app_publish_backend.run,
    )


@mock.patch("hamlet.command.run.expo_app_publish.run_expo_app_publish_backend")
def test_input_validation(run_expo_app_publish_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        run_expo_app_publish,
        run_expo_app_publish_backend.run,
        {
            "-u": "unit",
        },
        [],
    )
