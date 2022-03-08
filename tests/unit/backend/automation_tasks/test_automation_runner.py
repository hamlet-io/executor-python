from unittest import mock

from hamlet.backend.automation_tasks.base import AutomationRunner


def test_automation_runner_task(engine):
    """
    Tests that a task in the runner has been called
    """

    mock_task = mock.Mock()

    automation_runner = AutomationRunner(engine.engine)
    automation_runner._script_list = [
        {"func": mock_task, "args": {"mock_task_arg": "mock_task_arg_value"}}
    ]

    automation_runner.run()

    mock_task.assert_called_once_with(
        env=automation_runner._context_env,
        mock_task_arg="mock_task_arg_value",
        engine=engine.engine,
    )

    assert "AUTOMATION_PROVIDER" in automation_runner._context_env
    assert "AUTOMATION_DATA_DIR" in automation_runner._context_env
