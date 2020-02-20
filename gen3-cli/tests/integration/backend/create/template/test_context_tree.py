import os
import json
import tempfile
# import subprocess
from cot.backend.generate.cmdb import account, tenant
from cot.backend.generate.product import base
from cot.backend.create.template.environment import Environment
from cot.backend.create.template import context_tree as ct
from .conftest import conf


def test_find_gen3_dirs(clear_cmdb, cmdb):
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


class FSNode:

    def __init__(self, path):
        self.path = path

    def __getitem__(self, key):
        return self.__class__(os.path.join(self.path, key))

    def __setitem__(self, key, value):
        if not isinstance(value, str):
            value = json.dumps(value, indent=4)
        os.makedirs(self.path, exist_ok=True)
        with open(os.path.join(self.path, key), 'wt+') as f:
            f.write(value)

    def exists(self):
        return os.path.exists(self.path)

    def mkdir(self):
        os.makedirs(self.path, exist_ok=True)
        return self

    def mknod(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        os.mknod(self.path)

    def mkfile(self, data):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'wt+') as f:
            f.write(data)
        return self

    def mkjson(self, data):
        data = json.dumps(data)
        self.mkfile(data)

    def isfile(self):
        return os.path.isfile(self.path)

    def isdir(self):
        return os.path.isdir(self.path)

    def json(self):
        if self.isfile():
            with open(self.path, 'rt') as f:
                return json.load(f)
        raise TypeError(f'{self.path} is not a file')

    def text(self):
        if self.isfile():
            with open(self.path, 'rt') as f:
                return f.read()
        raise TypeError(f'{self.path} is not a file')


def test_upgrade_version_1_0_0():
    def create_test_fs(root):
        root = FSNode(root)

        root['build.ref'] = 'commit1 tag1'
        root['builds']['build.ref'] = 'commit2 tag2'

        root['shared-build.ref'] = 'reference1'
        root['shared-builds']['shared-build.ref'] = 'reference2'

        root['credentials.json'] = {'Credentials': ['1', '2']}
        root['credentials']['credentials.json'] = {'Credentials': ['3', '4']}

        root['container.json'] = {'Id': '1'}
        root['containers']['container.json'] = {'Id': '2'}

    def assert_post_upgrade_structure(root):
        root = FSNode(root)
        # Legacy
        assert not root['build.ref'].exists()
        assert not root['builds']['build.ref'].exists()

        assert not root['shared-build.ref'].exists()
        assert not root['shared-builds']['shared-build.ref'].exists()

        assert not root['container.json'].exists()
        assert not root['containers']['container.json'].exists()
        # Upgraded
        assert root['build.json'].json() == {
            'Commit': 'commit1',
            'Tag': 'tag1',
            'Formats': ['docker']
        }
        assert root['builds']['build.json'].json() == {
            'Commit': 'commit2',
            'Tag': 'tag2',
            'Formats': ['docker']
        }

        assert root['shared_build.json'].json() == {
            'Reference': 'reference1'
        }
        assert root['shared-builds']['shared_build.json'].json() == {
            'Reference': 'reference2'
        }

        assert root['credentials.json'].json() == [
            '1', '2'
        ]
        assert root['credentials']['credentials.json'].json() == [
            '3', '4'
        ]

        assert root['segment.json'].json() == {
            'Id': '1'
        }
        assert root['containers']['segment.json'].json() == {
            'Id': '2'
        }

    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        ct.upgrade_cmdb_repo_to_v1_0_0(root, '')
        ct.cleanup_cmdb_repo_to_v1_0_0(root, '')
        assert_post_upgrade_structure(root)


def test_upgrade_version_1_1_0():

    def create_test_fs(root):
        root = FSNode(root)

        appsettings = root['appsettings']
        appsettings['appsettings-file.json'].mknod()
        appsettings['appsettings-env']['subdir']['appsettings-env-sub-file.json'].mknod()
        appsettings['appsettings-env']['appsettings-env-file.json'].mknod()

        solutions = root['solutions']
        solutions['solutions-file.json'].mknod()
        solutions['segment.json'] = {
            'Segment': {
                'Environment': 'solutions',
                'Id': 'Id',
                'Name': 'Name',
                'Title': 'Title',
                'NonLegacyKey': 'NonLegacyKey'
            }
        }
        solutions['solutions-env']['subdir']['solutions-env-sub-file.json'].mknod()
        solutions['solutions-env']['solutions-env-file.json'].mknod()
        solutions['solutions-env']['segment.json'] = {
            'Segment': {
                'Environment': 'solutions-env',
                'Id': 'Id',
                'Name': 'Name',
                'Title': 'Title',
                'NonLegacyKey': 'NonLegacyKey'
            }
        }

        credentials = root['credentials']
        credentials['credentials-file.json'].mknod()
        credentials['aws-ssh.pem'].mknod()
        credentials['credentials-env']['subdir']['credentials-env-sub-file.json'].mknod()
        credentials['credentials-env']['credentials-env-file.json'].mknod()
        credentials['credentials-env']['.gitignore'] = 'test'
        credentials['credentials-env']['aws-ssh-env.pem'].mknod()

        aws = root['aws']
        aws['aws-file.json'].mknod()
        aws['cf']['aws-cf-file.json'].mknod()
        aws['aws-env']['subdir']['aws-env-sub-file.json'].mknod()
        aws['aws-env']['cf']['aws-env-cf-file.json'].mknod()
        aws['aws-env']['cf']['subdir']['aws-env-cf-sub-file.json'].mknod()

    def assert_post_upgrade_structure(root):
        root = FSNode(root)
        # Legacy
        assert not root['appsettings'].exists()
        # Upgraded
        settings = root['settings']
        assert settings['shared']['appsettings-file.json'].isfile()
        assert settings['appsettings-env']['default']['subdir']['appsettings-env-sub-file.json'].isfile()
        assert settings['appsettings-env']['default']['appsettings-env-file.json'].isfile()
        # Legacy
        assert not root['solutions'].exists()
        # Upgraded
        solutionsv2 = root['solutionsv2']
        assert solutionsv2.isdir()
        assert solutionsv2['shared']['default']['solutions-file.json'].isfile()
        assert solutionsv2['shared']['default']['segment.json'].json() == {
            'Segment': {
                'Id': 'default'
            }
        }
        assert solutionsv2['solutions-env']['default']['subdir']['solutions-env-sub-file.json'].isfile()
        assert solutionsv2['solutions-env']['default']['solutions-env-file.json'].isfile()
        assert solutionsv2['solutions-env']['default']['segment.json'].json() == {
            'Segment': {
                'NonLegacyKey': 'NonLegacyKey'
            }
        }
        assert solutionsv2['solutions-env']['environment.json'].json() == {
            'Environment': {
                'Id': 'solutions-env'
            }
        }
        # Legacy
        assert not root['credentials'].exists()
        # Upgraded
        operations = root['operations']
        assert operations['shared']['.aws-ssh.pem'].isfile()
        assert operations['shared']['.gitignore'].text() == '\n'.join(['*.plaintext', '*.decrypted', '*.ppk'])
        assert operations['shared']['credentials-file.json'].isfile()
        assert operations['credentials-env']['default']['subdir']['credentials-env-sub-file.json'].isfile()
        assert operations['credentials-env']['default']['credentials-env-file.json'].isfile()
        assert operations['credentials-env']['default']['.aws-ssh-env.pem'].isfile()
        assert operations['credentials-env']['default']['.gitignore'].text() == 'test'
        # Legacy
        cf = root['cf']
        assert not cf['shared']['aws-file.json'].isfile()
        assert cf['shared']['aws-cf-file.json'].isfile()
        assert cf['aws-env']['default']['aws-env-cf-file.json'].isfile()
        assert cf['aws-env']['default']['subdir']['aws-env-cf-sub-file.json'].isfile()
        assert not cf['aws-env']['default']['aws-env-sub-file.json'].exists()

    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        # subprocess.call('tree -a', shell=True, cwd=tmp_dir)
        ct.upgrade_cmdb_repo_to_v1_1_0(root, '')
        ct.cleanup_cmdb_repo_to_v1_1_0(root, '')
        # subprocess.call('tree -a', shell=True, cwd=tmp_dir)
        assert_post_upgrade_structure(root)
