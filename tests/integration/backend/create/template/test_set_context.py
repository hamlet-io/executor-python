import os

from hamlet.backend.generate.cmdb import account, tenant, product
from hamlet.backend.create.template.environment import Environment
from hamlet.backend.create.template.set_context import set_context
from .conftest import conf


def test(cmdb, clear_cmdb):
    clear_cmdb()

    tenant_id = conf["cmdb"]["tenant"]["tenant_id"]
    tenant_name = conf["cmdb"]["tenant"]["tenant_name"]
    account_id = conf["cmdb"]["account"]["account_id"]
    account_name = conf["cmdb"]["account"]["account_name"]
    product_id = conf["cmdb"]["product"]["product_id"]
    product_name = conf["cmdb"]["product"]["product_name"]

    with cmdb() as path:
        os.mknod("root.json")
        tenant.run(**conf["cmdb"]["tenant"], output_dir=path())
    with cmdb("accounts") as path:
        account.run(**conf["cmdb"]["account"], output_dir=path())
    with cmdb() as path:
        product.run(**conf["cmdb"]["product"], output_dir=path())
    with cmdb(product_name, "config") as path:
        e = Environment({"ACCOUNT": account_name})
        set_context(cwd=path(), environment_obj=e)

    with cmdb() as path:
        assert e.AID == account_id
        assert e.ACCOUNT == account_name
        assert e.ACCOUNT_DIR == os.path.join(path(), "accounts", account_name, "config")
        assert e.TID == tenant_id
        assert e.TENANT == tenant_name
        assert e.TENANT_DIR == os.path.join(path(), "accounts", tenant_name)
        assert e.PID == product_id
        assert e.PRODUCT == product_name
        assert e.PRODUCT_DIR == os.path.join(path(), product_name, "config")
        print(e)
