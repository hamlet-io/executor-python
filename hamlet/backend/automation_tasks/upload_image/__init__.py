from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    properties_file,
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
        engine=None,
        **kwargs
    ):

        _context_env = {
            "DEPLOYMENT_UNITS": deployment_unit,
            "GIT_COMMIT": build_reference,
            "IMAGE_FORMATS": image_format,
            "REGISTRY_SCOPE": registry_scope,
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
