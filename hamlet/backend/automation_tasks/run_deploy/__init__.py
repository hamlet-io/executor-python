from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_generation_context,
    manage_build_references,
    deploy
)

class RunDeployAutomationRunner(AutomationRunner):
    script_list = [
        {
            'func': set_generation_context.run,
            'args': {}
        },
        {
            'func': manage_build_references.run,
            'args': {
                'list': True
            }
        },
        {
            'func': deploy.run,
            'args': {}
        }
    ]
