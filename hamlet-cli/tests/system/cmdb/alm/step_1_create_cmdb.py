import os
import json
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
    with cmdb('accounts', 'tenant'):
        with open('domains.json', 'rb') as domains_file:
            domains_json = json.load(domains_file)
        product_name = conf['cmdb']['product']['product_name']
        tenant_name = conf['cmdb']['tenant']['tenant_name']
        domains_json['Certificates'][product_name] = {'Domain': tenant_name}
        with open('domains.json', 'wt') as domains_file:
            json.dump(domains_json, domains_file, indent=4)
