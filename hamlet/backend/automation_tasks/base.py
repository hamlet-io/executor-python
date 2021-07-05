import os
import tempfile
from abc import ABC

from hamlet.backend.automation.properties_file import get_automation_properties
from configparser import ConfigParser


class AutomationRunner(ABC):
    """
    Executes an automation based task
    """

    def __init__(self, **kwargs):
        self._context_env = kwargs
        self._script_list = []

    @staticmethod
    def _load_properties_to_context(properties_file):

        itemDict = {}

        if os.path.isfile(properties_file):
            config = ConfigParser(strict=False)

            s_config = open(properties_file, "r").read()
            s_config = f"[ini]\n{s_config}"

            config.read_string(s_config)
            items = config.items("ini")
            for key, value in items:
                itemDict[key] = value

        return itemDict

    def run(self):

        self._context_env["AUTOMATION_PROVIDER"] = "hamletcli"

        automation_properties = get_automation_properties(**self._context_env)
        self._context_env.update(automation_properties)

        with tempfile.TemporaryDirectory() as tmp_dir:

            self._context_env["AUTOMATION_DATA_DIR"] = tmp_dir

            for script in self._script_list:

                script["func"](env=self._context_env, **script["args"])
                script_context_envs = self._load_properties_to_context(
                    os.path.join(tmp_dir, "context.properties")
                )
                self._context_env = {**self._context_env, **script_context_envs}
