from hamlet.backend.generate.cmdb import account, tenant, product
from .conftest import conf


def run(cmdb, clear_cmdb):
    clear_cmdb()
    with cmdb() as path:
        tenant.run(**conf["cmdb"]["tenant"], output_dir=path())
    with cmdb("accounts") as path:
        account.run(**conf["cmdb"]["account"], output_dir=path())
    with cmdb() as path:
        product.run(**conf["cmdb"]["product"], output_dir=path())
