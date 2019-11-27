import os
from cookiecutter.main import cookiecutter
from cot import conf


TEMPLATES_DIR = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, 'cmdb')


def run(
    **kwargs
):
    template_path = os.path.join(TEMPLATES_DIR, 'tenant')
    cookiecutter(
        template_path,
        no_input=True,
        extra_context=kwargs
    )