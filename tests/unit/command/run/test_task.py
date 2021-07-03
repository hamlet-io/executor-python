import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.run.task import task as run_task
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS["!-i,--component"] = "container_name"
ALL_VALID_OPTIONS["!-w,--task"] = "task_name"
ALL_VALID_OPTIONS["!-t,--tier"] = "tier"
ALL_VALID_OPTIONS["-c,--container-id"] = "container_id"
ALL_VALID_OPTIONS["-d,--delay"] = 100
ALL_VALID_OPTIONS["-e,--env"] = "somevar"
ALL_VALID_OPTIONS["-j,--component-instance"] = "component_instance"
ALL_VALID_OPTIONS["-k,--component-version"] = "component_version"
ALL_VALID_OPTIONS["-v,--value"] = "value"
ALL_VALID_OPTIONS["-x,--instance"] = "task_instance"
ALL_VALID_OPTIONS["-y,--version"] = "task_version"


@mock.patch("hamlet.command.run.task.run_task_backend")
def test_input_valid(run_task_backend):
    run_options_test(CliRunner(), run_task, ALL_VALID_OPTIONS, run_task_backend.run)


@mock.patch("hamlet.command.run.task.run_task_backend")
def test_input_validation(run_task_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        run_task,
        run_task_backend.run,
        {
            "-i": "container_name",
            "-w": "task_name",
            "-t": "tier",
        },
        [("-d", "not_an_int", 10)],
    )
