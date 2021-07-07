from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_automation_context,
    manage_build_references,
    construct_tree,
)
from hamlet.backend.automation.properties_file import get_automation_properties


class TransferImageAutomationRunner(AutomationRunner):
    def __init__(
        self,
        source_account,
        source_environment,
        deployment_unit,
        build_reference,
        image_format,
        **kwargs
    ):
        super().__init__(**kwargs)

        self._source_account = source_account
        self._context_env = kwargs

        self._context_env["FROM_ACCOUNT"] = source_account
        self._context_env["FROM_ENVIRONMENT"] = source_environment

        self._script_list = [
            {
                "func": set_automation_context.run,
                "args": {"_is_cli": True, "release_mode": "promotion"},
            },
            {
                "func": construct_tree.run,
                "args": {
                    "exclude_account_dirs": True,
                    "exclude_product_dirs": True,
                    "use_existing_tree": True,
                    "_is_cli": True,
                },
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

    def run(self):

        source_args = {
            **self._context_env,
            **{
                "account": self._source_account,
            },
        }
        source_automation_properties = get_automation_properties(**source_args)
        self._context_env.update(source_automation_properties)

        return super().run()
