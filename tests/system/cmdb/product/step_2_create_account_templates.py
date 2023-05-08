import json
import os
from unittest import mock

from hamlet.backend.deploy import create_deployment as create_deployment_backend

from .conftest import conf

ACCOUNT = conf["cmdb"]["account"]["account_name"]
LEVEL = "account"


#  test is made accordingly to quickstart guide
@mock.patch.dict(os.environ, {"ACCOUNT": ACCOUNT, "DISTRICT_TYPE": "account"})
def run(cmdb, engine):
    with mock.patch.dict(os.environ, {"ROOT_DIR": cmdb.ROOT_DIR}):
        create_deployment_backend(
            deployment_group=LEVEL,
            deployment_unit="audit",
            deployment_mode="update",
            output_dir=None,
            engine=engine.engine,
        )
        create_deployment_backend(
            deployment_group=LEVEL,
            deployment_unit="s3",
            deployment_mode="update",
            output_dir=None,
            engine=engine.engine,
        )

        #  check that files were created
        with cmdb(
            "accounts", ACCOUNT, "infrastructure", "cf", "shared", "s3", "default"
        ) as filename:

            def prefix(level):
                return [
                    LEVEL,
                    level,
                    ACCOUNT,
                    conf["cmdb"]["tenant"]["default_region"],
                ]

            assert os.path.exists(
                filename(*prefix("s3"), "generation-contract", sep="-", ext="json")
            )

            cf_s3_template_filename = filename(
                *prefix("s3"), "template", sep="-", ext="json"
            )

            assert os.path.exists(cf_s3_template_filename)
            with open(cf_s3_template_filename) as f:
                json.load(f)

        with cmdb(
            "accounts", ACCOUNT, "infrastructure", "cf", "shared", "audit", "default"
        ) as filename:

            def prefix(level):
                return [
                    LEVEL,
                    level,
                    ACCOUNT,
                    conf["cmdb"]["tenant"]["default_region"],
                ]

            assert os.path.exists(
                filename(*prefix("audit"), "generation-contract", sep="-", ext="json")
            )

            cf_audit_template_filename = filename(
                *prefix("audit"), "template", sep="-", ext="json"
            )

            assert os.path.exists(cf_audit_template_filename)
            with open(cf_audit_template_filename) as f:
                json.load(f)
