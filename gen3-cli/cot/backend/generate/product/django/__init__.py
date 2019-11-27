import os
from cookiecutter.main import cookiecutter
from cot import conf


TEMPLATES_DIR = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, 'products')


def run(
    **kwargs
):
    for key, value in kwargs.items():
        if value is None:
            kwargs[key] = ''

    kwargs['use_celery'] = 'yes' if kwargs['use_celery'] else 'no'
    kwargs['allow_user_registration'] = 'yes' if kwargs['allow_user_registration'] else 'no'
    kwargs['alerts_use_ktlg'] = 'yes' if kwargs['alerts_use_ktlg'] else 'no'
    kwargs['alerts_use_email'] = 'yes' if kwargs['alerts_use_email'] else 'no'

    template_path = os.path.join(TEMPLATES_DIR, 'django-cookiecutter')
    cookiecutter(
        template_path,
        no_input=True,
        extra_context=kwargs
    )
