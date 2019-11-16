import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.run.task import task as run_task
from tests.unit.command.test_option_generation import generate_test_options_collection


ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-i,--component'] = 'container_name'
ALL_VALID_OPTIONS['!-w,--task'] = 'task_name'
ALL_VALID_OPTIONS['!-t,--tier'] = 'tier'
ALL_VALID_OPTIONS['-c,--container-id'] = 'container_id'
ALL_VALID_OPTIONS['-d,--delay'] = 100
ALL_VALID_OPTIONS['-e,--env'] = 'somevar'
ALL_VALID_OPTIONS['-j,--component-instance'] = 'component_instance'
ALL_VALID_OPTIONS['-k,--component-version'] = 'component_version'
ALL_VALID_OPTIONS['-v,--value'] = 'value'
ALL_VALID_OPTIONS['-x,--instance'] = 'task_instance'
ALL_VALID_OPTIONS['-y,--version'] = 'task_version'


@mock.patch('cot.command.run.task.subprocess')
def test_input_valid(subprocess_mock):
    assert len(ALL_VALID_OPTIONS) == len(run_task.params)
    runner = CliRunner()
    for args in generate_test_options_collection(ALL_VALID_OPTIONS):
        result = runner.invoke(run_task, args)
        assert result.exit_code == 0, result.output
        assert subprocess_mock.run.call_count == 1
        subprocess_mock.run.call_count = 0
