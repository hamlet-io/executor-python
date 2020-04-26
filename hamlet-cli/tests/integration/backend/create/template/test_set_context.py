import os
import json
from hamlet.backend.generate.cmdb import account, tenant
from hamlet.backend.generate.product import base
from hamlet.backend.create.template.environment import Environment
from hamlet.backend.create.template.set_context import set_context
from .conftest import conf


def test(cmdb, clear_cmdb):
    clear_cmdb()

    tenant_id = conf['cmdb']['tenant']['tenant_id']
    tenant_name = conf['cmdb']['tenant']['tenant_name']
    account_id = conf['cmdb']['account']['account_id']
    account_name = conf['cmdb']['account']['account_name']
    product_id = conf['cmdb']['product']['product_id']
    product_name = conf['cmdb']['product']['product_name']

    with cmdb():
        os.mknod('root.json')
        tenant.run(**conf['cmdb']['tenant'])
    with cmdb('accounts'):
        account.run(**conf['cmdb']['account'])
    with cmdb():
        base.run(**conf['cmdb']['product'])
    with cmdb('accounts', tenant_name):
        with open('domains.json', 'rb') as domains_file:
            domains_json = json.load(domains_file)
        domains_json['Certificates'][product_name] = {'Domain': tenant_name}
        with open('domains.json', 'wt') as domains_file:
            json.dump(domains_json, domains_file, indent=4)

    with cmdb(product_name, 'config') as path:
        e = Environment({'ACCOUNT': account_name})
        set_context(cwd=path(), environment_obj=e)

    with cmdb() as path:
        assert e.AID == account_id
        assert e.ACCOUNT == account_name
        assert e.ACCOUNT_DIR == os.path.join(path(), 'accounts', account_name, 'config')
        assert e.TID == tenant_id
        assert e.TENANT == tenant_name
        assert e.TENANT_DIR == os.path.join(path(), 'accounts', tenant_name)
        assert e.PID == product_id
        assert e.PRODUCT == product_name
        assert e.PRODUCT_DIR == os.path.join(path(), product_name, 'config')
        print(e)
