from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_automation_context,
    construct_tree,
    manage_images,
)


class UploadImageAutomationRunner(AutomationRunner):
    """
    Runs the automation tasks required to upload an image into a registry
    """

    def __init__(
        self,
        deployment_unit=None,
        build_reference=None,
        image_format=None,
        image_path=None,
        dockerfile=None,
        docker_context=None,
        docker_image=None,
        registry_scope=None,
        **kwargs
    ):
        super().__init__()

        self._context_env = kwargs

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
            {
                "func": manage_images.run,
                "args": {
                    "registry_scope": registry_scope,
                    "dockerfile": dockerfile,
                    "docker_context": docker_context,
                    "image_formats": image_format,
                    "code_commit": build_reference,
                    "image_paths": image_path,
                    "docker_image": docker_image,
                    "deployment_unit": deployment_unit,
                    "_is_cli": True,
                },
            },
        ]
