import os
import json
from cot.backend.generate.cmdb import account, tenant
from cot.backend.generate.product import base
from cot.backend.create.template.environment import Environment
from cot.backend.create.template import context_tree as ct
from .conftest import conf


def test(clear_cmdb, cmdb):
    clear_cmdb()

    tenant_name = conf['cmdb']['tenant']['tenant_name']
    account_name = conf['cmdb']['account']['account_name']
    product_name = conf['cmdb']['product']['product_name']
    segment_name = conf['cmdb']['product']['segment_name']
    environment_name = conf['cmdb']['product']['environment_name']

    with cmdb() as path:
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

    with cmdb() as path:
        root_dir = path()
        assert root_dir == ct.find_gen3_root_dir(path())
        tenant_dir = os.path.join(root_dir, 'accounts', tenant_name)
        assert tenant_dir == ct.find_gen3_tenant_dir(root_dir, tenant_name)
        account_base_dir = os.path.join(root_dir, 'accounts', account_name)
        account_dir = os.path.join(account_base_dir, 'config')
        account_infr_dir = os.path.join(account_base_dir, 'infrastructure')
        assert account_dir == ct.find_gen3_account_dir(root_dir, account_name)
        assert account_infr_dir == ct.find_gen3_account_infrastructure_dir(root_dir, account_name)
        product_base_dir = os.path.join(root_dir, product_name)
        product_dir = os.path.join(product_base_dir, 'config')
        product_infr_dir = os.path.join(product_base_dir, 'infrastructure')
        environment_dir = os.path.join(product_dir, 'solutionsv2', environment_name)
        assert product_dir == ct.find_gen3_product_dir(root_dir, product_name)
        assert product_infr_dir == ct.find_gen3_product_infrastructure_dir(root_dir, product_name)
        assert environment_dir == ct.find_gen3_environment_dir(root_dir, product_name, environment_name)
        e = Environment()
        ct.find_gen3_dirs(
            e,
            root_dir,
            tenant=tenant_name,
            account=account_name,
            product=product_name,
            environment=environment_name,
            segment=segment_name
        )
        assert e.ROOT_DIR == root_dir
        assert e.TENANT_DIR == tenant_dir

        assert e.ACCOUNT_DIR == account_dir
        assert e.ACCOUNT_INFRASTRUCTURE_DIR == account_infr_dir
        assert e.ACCOUNT_SETTINGS_DIR == os.path.join(account_dir, 'settings')
        assert e.ACCOUNT_OPERATIONS_DIR == os.path.join(account_infr_dir, 'operations')
        product_settings_dir = os.path.join(product_dir, 'settings')
        product_operations_dir = os.path.join(product_infr_dir, 'operations')
        product_solutions_dir = os.path.join(product_dir, 'solutionsv2')
        environment_shared_operations_dir = os.path.join(product_infr_dir, 'operations', environment_name)
        environment_shared_settings_dir = os.path.join(product_dir, 'settings', environment_name)
        environment_shared_solutions_dir = os.path.join(product_dir, 'solutionsv2', environment_name)
        segment_solutions_dir = os.path.join(product_dir, 'solutionsv2', environment_name, segment_name)
        segment_settings_dir = os.path.join(product_dir, 'settings', environment_name, segment_name)
        segment_operations_dir = os.path.join(product_infr_dir, 'operations', environment_name, segment_name)
        segment_builds_dir = segment_settings_dir
        segment_shared_settings_dir = os.path.join(product_dir, 'settings', 'shared', segment_name)
        segment_shared_solutions_dir = os.path.join(product_dir, 'solutionsv2', 'shared', segment_name)
        segment_shared_operations_dir = os.path.join(product_infr_dir, 'operations', 'shared', segment_name)
        assert e.PRODUCT_DIR == product_dir
        assert e.PRODUCT_SETTINGS_DIR == product_settings_dir
        assert e.PRODUCT_INFRASTRUCTURE_DIR == product_infr_dir
        assert e.PRODUCT_OPERATIONS_DIR == product_operations_dir
        assert e.PRODUCT_SOLUTIONS_DIR == product_solutions_dir
        assert e.PRODUCT_SHARED_SETTINGS_DIR == os.path.join(product_settings_dir, 'shared')
        assert e.PRODUCT_SHARED_OPERATIONS_DIR == os.path.join(product_operations_dir, 'shared')
        assert e.PRODUCT_SHARED_SOLUTIONS_DIR == os.path.join(product_solutions_dir, 'shared')
        assert e.ENVIRONMENT_SHARED_SETTINGS_DIR == environment_shared_settings_dir
        assert e.ENVIRONMENT_SHARED_SOLUTIONS_DIR == environment_shared_solutions_dir
        assert e.ENVIRONMENT_SHARED_OPERATIONS_DIR == environment_shared_operations_dir
        assert e.SEGMENT_SOLUTIONS_DIR == segment_solutions_dir
        assert e.SEGMENT_SETTINGS_DIR == segment_settings_dir
        assert e.SEGMENT_OPERATIONS_DIR == segment_operations_dir
        assert e.SEGMENT_BUILDS_DIR == segment_builds_dir
        assert e.SEGMENT_SHARED_SETTINGS_DIR == segment_shared_settings_dir
        assert e.SEGMENT_SHARED_SOLUTIONS_DIR == segment_shared_solutions_dir
        assert e.SEGMENT_SHARED_OPERATIONS_DIR == segment_shared_operations_dir
        print(e)
