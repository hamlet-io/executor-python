from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_generation_context,
    confirm_builds,
    update_build_references
)

class UpdateBuildAutomationRunner(AutomationRunner):
    def __init__(
            self,
            product,
            environment,
            segment,
            deployment_units,
            git_commit,
            code_tag=None
        ):
        super().__init__()

        self._context_env['PRODUCT'] = product
        self._context_env['ENVIRONMENT'] = environment
        self._context_env['SEGMENT'] = segment
        self._context_env['DEPLOYMENT_UNITS'] = deployment_units
        self._context_env['GIT_COMMIT'] = git_commit
        self._context_env['CODE_TAG'] = code_tag


    script_list = [
        {
            'func': set_generation_context.run,
            'args': {}
        },
        {
            'func': confirm_builds.run,
            'args': {}
        },
        {
            'func': update_build_references.run,
            'args': {}
        }
    ]
