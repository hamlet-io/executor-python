import os
import json
from unittest import mock

from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.deploy import create_deployment as create_deployment_backend
from .conftest import conf


ACCOUNT = conf["cmdb"]["account"]["account_name"]
LEVEL = "account"


#  test is made accordingly to quickstart guide
@mock.patch.dict(os.environ, {"ACCOUNT": ACCOUNT})
def run(cmdb, engine):

    global_engine_env = engine.engine_store.get_engine(ENGINE_GLOBAL_NAME).environment

    with mock.patch.dict(os.environ, {"ROOT_DIR": cmdb.ROOT_DIR, **global_engine_env}):

        create_deployment_backend(
            deployment_group=LEVEL,
            deployment_unit="audit",
            deployment_mode="update",
            output_dir=None,
        )
        create_deployment_backend(
            deployment_group=LEVEL,
            deployment_unit="s3",
            deployment_mode="update",
            output_dir=None,
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
                filename(*prefix("s3"), "epilogue", sep="-", ext="sh")
            )

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
