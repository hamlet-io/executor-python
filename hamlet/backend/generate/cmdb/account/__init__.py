import random
import string
from hamlet.backend.generate import utils
from . import template as account_cmdb_template


def generate_account_seed():
    seed = list(string.ascii_lowercase + string.digits)
    random.shuffle(seed)
    return "".join(seed[:10])


def run(**kwargs):
    utils.cookiecutter(account_cmdb_template, **kwargs)
