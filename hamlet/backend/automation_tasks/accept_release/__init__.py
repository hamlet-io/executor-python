from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_context,
    construct_tree,
    accept_release
)

class AcceptReleaseAutomationRunner(AutomationRunner):
    script_list = [
        {
            'func': set_context.run(),
            'args': {}
        },
        {
            'func': construct_tree.run(),
            'args': {}
        },
        {
            'func': accept_release.run(),
            'args': {}
        }
    ]
