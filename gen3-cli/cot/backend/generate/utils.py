import os
from cookiecutter.main import cookiecutter as cookiecutter_main
from cot import conf


def replace_parameters_values(kwargs, replacers=None):
    for key, value in kwargs.items():
        for target, replacer in replacers:
            if value is target or value == target:
                kwargs[key] = replacer
                break


def cookiecutter(*template_path, **kwargs):
    replace_parameters_values(
        kwargs,
        [
            [None, ''],
            [True, 'yes'],
            [False, 'no']
        ]
    )
    template_path = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, *template_path)
    cookiecutter_main(
        template_path,
        no_input=True,
        extra_context=kwargs
    )
