from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    properties_file,
    set_automation_context,
    construct_tree,
    manage_build_references,
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
            {
                "func": manage_build_references.run,
                "args": {
                    "_is_cli": True,
                    "verify": "latest",
                    "code_commits": build_reference,
                    "deployment_units": deployment_unit,
                    "image_formats": image_format,
                    "code_tags": code_tag,
                    "registry_scopes": registry_scope,
                },
            },
            {
                "func": manage_build_references.run,
                "args": {
                    "_is_cli": True,
                    "update": True,
                    "code_commits": build_reference,
                    "deployment_units": deployment_unit,
                    "image_formats": image_format,
                    "code_tags": code_tag,
                    "registry_scopes": registry_scope,
                },
            },
        ]
