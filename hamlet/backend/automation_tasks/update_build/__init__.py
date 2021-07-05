from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_automation_context,
    construct_tree,
    confirm_builds,
    update_build_references,
)


class UpdateBuildAutomationRunner(AutomationRunner):
    def __init__(
        self,
        deployment_unit=None,
        build_reference=None,
        code_tag=None,
        image_format=None,
        registry_scope=None,
        **kwargs
    ):
        super().__init__()

        self._context_env = {
            "DEPLOYMENT_UNITS": deployment_unit,
            "GIT_COMMIT": build_reference,
            "CODE_TAGS": code_tag,
            "IMAGE_FORMATS": image_format,
            "REGISTRY_SCOPE": registry_scope,
            **kwargs,
        }

        self._script_list = [
            {"func": set_automation_context.run, "args": {"_is_cli": True}},
            {
                "func": construct_tree.run,
                "args": {
                    "exclude_account_dirs": True,
                    "exclude_product_dirs": True,
                    "use_existing_tree": True,
                    "_is_cli": True,
                },
            },
            {"func": confirm_builds.run, "args": {"_is_cli": True}},
            {"func": update_build_references.run, "args": {"_is_cli": True}},
        ]
