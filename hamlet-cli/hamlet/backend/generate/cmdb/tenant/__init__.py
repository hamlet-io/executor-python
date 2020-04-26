from hamlet.backend.generate import utils


def run(**kwargs):
    utils.cookiecutter('cmdb', 'tenant', **kwargs)
