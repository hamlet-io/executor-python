from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    properties_file,
    set_automation_context,
    manage_build_references,
    construct_tree,
)


class TransferImageAutomationRunner(AutomationRunner):
    def __init__(
        self,
        source_account,
        source_environment,
        deployment_unit,
        build_reference,
        image_format,
        engine,
        **kwargs
    ):
        _context_env = {
            "DEPLOYMENT_UNITS": deployment_unit,
            "IMAGE_FORMATS": image_format,
            "GIT_COMMIT": build_reference,
            "FROM_ACCOUNT": source_account,
            "FROM_ENVIRONMENT": source_environment,
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
            {
                "func": properties_file.get_automation_properties,
                "args": {
                    **self._context_env,
                    "account": source_account,
                    "environment": source_environment,
                },
            },
            {
                "func": set_automation_context.run,
                "args": {"_is_cli": True, "release_mode": "promotion"},
            },
            {
                "func": manage_build_references.run,
                "args": {
                    "verify": "latest",
                    "code_commits": build_reference,
                    "deployment_units": deployment_unit,
                    "image_formats": image_format,
                    "_is_cli": True,
                },
            },
        ]
