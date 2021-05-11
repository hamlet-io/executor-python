from hamlet.backend.generate import utils
from . import template as product_cmdb_template


def run(**kwargs):

    utils.cookiecutter(product_cmdb_template, **kwargs)
