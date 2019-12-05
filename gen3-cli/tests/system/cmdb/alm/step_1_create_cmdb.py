from cot.backend.generate.cmdb import account, tenant
from cot.backend.generate.product import app_lifecycle_mgmt
from .conftest import conf


def test_cmdb_creation(cmdb, clear_cmdb):
    clear_cmdb()
    with cmdb():
        tenant.run(**conf['cmdb']['tenant'])
    with cmdb('accounts'):
        account.run(**conf['cmdb']['account'])
    with cmdb():
        app_lifecycle_mgmt.run(**conf['cmdb']['product'])
