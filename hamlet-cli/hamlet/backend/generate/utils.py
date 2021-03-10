import os
from cookiecutter.main import cookiecutter as cookiecutter_main
from hamlet import env


def replace_parameters_values(kwargs, replacers=None):
    for key, value in kwargs.items():
        for target, replacer in replacers:
            if value is target or value == target:
                kwargs[key] = replacer
                break


def cookiecutter(*template_path, output_dir, **kwargs):
    replace_parameters_values(
        kwargs,
        [
            [None, ''],
            [True, 'yes'],
            [False, 'no']
        ]
    )
    template_path = os.path.join(env.GENERATION_PATTERNS_DIR, *template_path)
    cookiecutter_main(
        template_path,
        no_input=True,
        output_dir=output_dir,
        extra_context=kwargs
    )
