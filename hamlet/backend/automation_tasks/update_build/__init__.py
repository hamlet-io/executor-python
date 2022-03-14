from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    properties_file,
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
        engine=None,
        **kwargs
    ):
        _context_env = {
            "DEPLOYMENT_UNITS": deployment_unit,
            "GIT_COMMIT": build_reference,
            "CODE_TAGS": code_tag,
            "IMAGE_FORMATS": image_format,
            "REGISTRY_SCOPE": registry_scope,
            "DEFER_REPO_PUSH": "true",
            **kwargs,
        }

        super().__init__(engine=engine, **_context_env)

        self._script_list = [
            {
                "func": construct_tree.run,
                "args": {
                    "use_existing_tree": True,
                    "_is_cli": True,
                },
            },
            {
                "func": properties_file.get_automation_properties,
                "args": {**self._context_env},
            },
            {"func": set_automation_context.run, "args": {"_is_cli": True}},
            {"func": confirm_builds.run, "args": {"_is_cli": True}},
            {"func": update_build_references.run, "args": {"_is_cli": True}},
        ]
