from hamlet.backend.automation_tasks.base import AutomationRunner
from hamlet.backend.automation import (
    set_generation_context,
    manage_images,
)

class ManageImagesAutomationRunner(AutomationRunner):
    def __init__(self,
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

        self._context_env = { **kwargs }

        self._script_list = [
            {
                'func': set_generation_context.run,
                'args': {}
            },
            {
                'func': manage_images.run,
                'args': {
                    'registry_scope': registry_scope,
                    'dockerfile' : dockerfile,
                    'docker_context': docker_context,
                    'image_formats': image_format,
                    'code_commit': build_reference,
                    'image_paths': image_path,
                    'docker_image': docker_image,
                    'deployment_unit' : deployment_unit,
                    '_is_cli' : True
                }
            }
        ]
