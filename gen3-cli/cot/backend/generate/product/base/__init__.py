from cot.backend.generate import utils


def run(**kwargs):
    utils.cookiecutter('products', 'base', **kwargs)
