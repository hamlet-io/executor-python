from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_automation_context,
    construct_tree,
    save_cmdb_repos,
)


class SaveCMDBAutomationRunner(AutomationRunner):
    def __init__(
        self,
        account_repos,
        commit_message,
        product_repos,
        reference,
        tag,
        defer_push,
        engine,
        **kwargs
    ):
        super().__init__(engine=engine, **kwargs)

        self._script_list = [
            {
                "func": construct_tree.run,
                "args": {
                    "use_existing_tree": True,
                    "_is_cli": True,
                },
            },
            {
                "func": set_automation_context.run,
                "args": {"_is_cli": True, "context_credentials": False},
            },
            {
                "func": save_cmdb_repos.run,
                "args": {
                    "account_repos": account_repos,
                    "commit_message": commit_message,
                    "product_repos": product_repos,
                    "reference": reference,
                    "defer_push": defer_push,
                    "tag": tag,
                    "_is_cli": True,
                },
            },
        ]
