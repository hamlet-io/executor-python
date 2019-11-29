import random
import string
from cot.backend.generate import utils


def generate_account_seed():
    seed = list(string.ascii_lowercase + string.digits)
    random.shuffle(seed)
    return ''.join(seed[:10])


def run(**kwargs):
    utils.cookiecutter('cmdb', 'account', **kwargs)
