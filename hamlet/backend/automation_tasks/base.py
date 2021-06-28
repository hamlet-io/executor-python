import os
from abc import ABC

from configparser import ConfigParser

class AutomationRunner(ABC):
    '''
    Executes an automation based task
    '''

    def __init__(self, product_properties_file, work_dir):
        self.product_properties_file = product_properties_file
        self.work_dir = work_dir

        self._context_env = {}

    @staticmethod
    def _load_properties_to_context(self, properties_file):
        config = ConfigParser()

        s_config= open(properties_file, 'r').read()
        s_config=f"[ini]\n{s_config}"

        config.read_string(s_config)
        items=config.items('ini')
        itemDict={}
        for key,value in items:
            itemDict[key]=value
        self._context_env = { **self._context_env, **itemDict}

    script_list = []

    def run(self):
        self._load_properties_to_context(self.product_properties_file)

        for script in self.script_list:
            script['func'](env=self._context_env **script['args'])
            self._load_properties_to_context(os.path.join(self.work_dir, 'context.properties'))