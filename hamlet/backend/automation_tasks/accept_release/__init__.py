from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_generation_context,
    accept_release
)

class AcceptReleaseAutomationRunner(AutomationRunner):
    script_list = [
        {
            'func': set_generation_context.run,
            'args': {}
        },
        {
            'func': accept_release.run,
            'args': {}
        }
    ]
