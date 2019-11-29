from cot.backend.generate import utils


def run(**kwargs):
    utils.cookiecutter('cmdb', 'tenant', **kwargs)
