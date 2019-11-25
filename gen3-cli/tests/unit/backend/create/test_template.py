import os
import json
from unittest import mock
from cot.backend.create import template as create_template_backend


TENANT = 'test_tenant'
ACCOUNT = 'test_account'
PRODUCT = 'test_product'


#  test is made accordingly to quickstart guide
@mock.patch.dict(
    os.environ,
    {
        'ACCOUNT': ACCOUNT,
        'GENERATION_INPUT_SOURCE_DEFAULT': 'mock'
    }
)
def test_account(cmdb, clear_cmdb_dir):
    # clearing all dirs which should be empty on fresh start
    clear_cmdb_dir('cache')
    clear_cmdb_dir('accounts', ACCOUNT, 'infrastructure')

    # reading region because it the part of the filenames
    with cmdb('accounts', TENANT):
        with open('tenant.json') as f:
            tenant_json = json.load(f)

    account_region = tenant_json['Account']['Region']

    # cd to level dir
    with cmdb('accounts', ACCOUNT, 'config'):
        create_template_backend.run(
            level='account',
            deployment_unit='audit'
        )
        create_template_backend.run(
            level='account',
            deployment_unit='s3'
        )

    #  check that files were created
    with cmdb('accounts', ACCOUNT, 'infrastructure', 'cf', 'shared') as filename:
        prefix = [
            'account',
            's3',
            ACCOUNT,
            account_region,
        ]
        assert os.path.exists(
            filename(
                *prefix,
                'epilogue',
                sep='-',
                ext='sh'
            )
        )
        assert os.path.exists(
            filename(
                *prefix,
                'genplan',
                sep='-',
                ext='sh'
            )
        )

        cf_template_filename = filename(
            *prefix,
            'template',
            sep='-',
            ext='json'
        )

        assert os.path.exists(cf_template_filename)
        with open(cf_template_filename) as f:
            json.load(f)
