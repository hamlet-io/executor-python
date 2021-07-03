from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_generation_context,
    set_automation_context,
    manage_build_references
)

class TransferReleaseAutomationRunner(AutomationRunner):
    script_list = [
        {
            'func': set_generation_context.run,
            'args': {}
        },
        {
            'func': set_automation_context.run,
            'args': {
                'release_mode' : 'promotion'
            }
        },
        {
            'func': manage_build_references.run,
            'args': {
                'verify': 'latest'
            }
        }
    ]
