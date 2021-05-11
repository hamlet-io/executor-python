from hamlet.backend.generate import utils
from . import template as tenant_cmdb_template


def run(**kwargs):

    utils.cookiecutter(tenant_cmdb_template, **kwargs)
