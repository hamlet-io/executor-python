import os
from cookiecutter.main import cookiecutter
from cot import conf
from cot.backend.generate import utils


TEMPLATES_DIR = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, 'cmdb')


def run(**kwargs):
    utils.replace_parameters_values(
        kwargs,
        [
            [None, ''],
            [True, 'yes'],
            [False, 'no']
        ]
    )
    template_path = os.path.join(TEMPLATES_DIR, 'tenant')
    cookiecutter(
        template_path,
        no_input=True,
        extra_context=kwargs
    )
