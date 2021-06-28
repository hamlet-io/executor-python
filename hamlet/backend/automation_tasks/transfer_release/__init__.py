from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_context,
    construct_tree,
    manage_build_references
)

class TransferReleaseAutomationRunner(AutomationRunner):
    script_list = [
        {
            'func': set_context.run,
            'args': {
                'release_mode' : 'promotion'
            }
        },
        {
            'func': construct_tree.run,
            'args': {}
        },
        {
            'func': manage_build_references.run,
            'args': {
                'verify': 'latest'
            }
        }
    ]
