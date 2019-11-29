from cot.backend.generate import utils


def run(**kwargs):
    utils.cookiecutter('products', 'app-lifecycle-mgmt', **kwargs)
