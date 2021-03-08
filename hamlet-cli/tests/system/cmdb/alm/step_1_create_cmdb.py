import os
from hamlet.backend.generate.cmdb import account, tenant
from hamlet.backend.generate.product import app_lifecycle_mgmt
from .conftest import conf


def run(cmdb, clear_cmdb):
    clear_cmdb()
    with cmdb() as path:
        os.mknod('root.json')
        tenant.run(**conf['cmdb']['tenant'], output_dir=path())
    with cmdb('accounts') as path:
        account.run(**conf['cmdb']['account'], output_dir=path())
    with cmdb() as path:
        app_lifecycle_mgmt.run(**conf['cmdb']['product'], output_dir=path())
