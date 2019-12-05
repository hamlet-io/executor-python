import os
import json
from unittest import mock
from cot.backend.create import template as create_template_backend
from .conftest import conf


ACCOUNT = conf['cmdb']['account']['account_name']
LEVEL = 'account'


#  test is made accordingly to quickstart guide
@mock.patch.dict(
    os.environ,
    {
        'ACCOUNT': ACCOUNT
    }
)
def run(cmdb):
    with cmdb('accounts', ACCOUNT, 'config'):
        create_template_backend.run(
            level=LEVEL,
            deployment_unit='audit'
        )
        create_template_backend.run(
            level=LEVEL,
            deployment_unit='s3'
        )

    #  check that files were created
    with cmdb('accounts', ACCOUNT, 'infrastructure', 'cf', 'shared') as filename:

        def prefix(level):
            return [
                LEVEL,
                level,
                ACCOUNT,
                conf['cmdb']['tenant']['default_region'],
            ]

        assert os.path.exists(
            filename(
                *prefix('s3'),
                'epilogue',
                sep='-',
                ext='sh'
            )
        )
        assert os.path.exists(
            filename(
                *prefix('s3'),
                'genplan',
                sep='-',
                ext='sh'
            )
        )

        assert os.path.exists(
            filename(
                *prefix('audit'),
                'genplan',
                sep='-',
                ext='sh'
            )
        )

        cf_s3_template_filename = filename(
            *prefix('s3'),
            'template',
            sep='-',
            ext='json'
        )

        cf_audit_template_filename = filename(
            *prefix('audit'),
            'template',
            sep='-',
            ext='json'
        )

        assert os.path.exists(cf_s3_template_filename)
        assert os.path.exists(cf_audit_template_filename)
        with open(cf_s3_template_filename) as f:
            json.load(f)
        with open(cf_audit_template_filename) as f:
            json.load(f)
