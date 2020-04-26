from hamlet.backend.generate import utils


def run(**kwargs):
    utils.cookiecutter('products', 'django-cookiecutter', **kwargs)
