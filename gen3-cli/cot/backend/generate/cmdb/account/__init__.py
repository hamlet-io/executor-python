import os
import random
import string
from cookiecutter.main import cookiecutter
from cot import conf


TEMPLATES_DIR = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, 'cmdb')


def generate_account_seed():
    seed = list(string.ascii_lowercase + string.digits)
    random.shuffle(seed)
    return ''.join(seed[:10])


def run(
    **kwargs
):
    template_path = os.path.join(TEMPLATES_DIR, 'account')
    cookiecutter(
        template_path,
        no_input=True,
        extra_context=kwargs
    )
