import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.entrance import invoke_entrance as invoke_entrance
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS["!-e,--entrance"] = "entrance"
ALL_VALID_OPTIONS["-l,--deployment-group"] = "deployment_group"
ALL_VALID_OPTIONS["-u,--deployment-unit"] = "deployment_unit"
ALL_VALID_OPTIONS["-z,--deployment-unit-subset"] = "deployment_unit_subset"
ALL_VALID_OPTIONS["-d,--deployment-mode"] = "deployment_mode"
ALL_VALID_OPTIONS["-x,--disable-output-cleanup"] = [True]
ALL_VALID_OPTIONS["-o,--output-dir"] = "output_dir"
ALL_VALID_OPTIONS["-c,--config-ref"] = "config_ref"
ALL_VALID_OPTIONS["-q,--request-ref"] = "request_ref"


@mock.patch("hamlet.command.entrance.create_template_backend")
def test_input_valid(create_template_backend):
    run_options_test(
        CliRunner(), invoke_entrance, ALL_VALID_OPTIONS, create_template_backend.run
    )


@mock.patch("hamlet.command.entrance.create_template_backend")
def test_input_validation(create_template_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner, invoke_entrance, create_template_backend.run, {"-e": "blueprint"}, []
    )
