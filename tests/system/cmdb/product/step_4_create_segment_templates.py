import os
import json
from unittest import mock

from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.deploy import create_deployment as create_deployment_backend
from .conftest import conf


TENANT = conf["cmdb"]["tenant"]["tenant_name"]
ACCOUNT = conf["cmdb"]["account"]["account_name"]
PRODUCT = conf["cmdb"]["product"]["product_name"]
ENVIRONMENT = conf["cmdb"]["product"]["environment_name"]
SEGMENT = conf["cmdb"]["product"]["segment_name"]

LEVEL = "segment"


#  test is made accordingly to quickstart guide
@mock.patch.dict(
    os.environ,
    {
        "TENANT": TENANT,
        "ACCOUNT": ACCOUNT,
        "PRODUCT": PRODUCT,
        "ENVIRONMENT": ENVIRONMENT,
        "SEGMENT": SEGMENT,
    },
)
def run(cmdb, engine):
    global_engine_env = engine.engine_store.get_engine(ENGINE_GLOBAL_NAME).environment
    with mock.patch.dict(os.environ, {"ROOT_DIR": cmdb.ROOT_DIR, **global_engine_env}):

        create_deployment_backend(
            deployment_group=LEVEL,
            deployment_unit="baseline",
            deployment_mode="update",
            output_dir=None,
        )

        #  check that files were created
        with cmdb(
            PRODUCT, "infrastructure", "cf", ENVIRONMENT, SEGMENT, "baseline", "default"
        ) as filename:

            def prefix(unit):

                level_prefix = LEVEL
                if LEVEL == "segment":
                    level_prefix = "seg"

                return [
                    level_prefix,
                    unit,
                    ACCOUNT,
                    conf["cmdb"]["tenant"]["default_region"],
                ]

            assert os.path.exists(
                filename(*prefix("baseline"), "epilogue", sep="-", ext="sh")
            )

            assert os.path.exists(
                filename(
                    *prefix("baseline"), "generation-contract", sep="-", ext="json"
                )
            )

            cf_baseline_template_filename = filename(
                *prefix("baseline"), "template", sep="-", ext="json"
            )

            assert os.path.exists(cf_baseline_template_filename)
            with open(cf_baseline_template_filename) as f:
                json.load(f)
