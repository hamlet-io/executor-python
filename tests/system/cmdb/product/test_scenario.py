from . import step_1_create_cmdb
from . import step_2_create_account_templates
from . import step_3_create_segment_templates


def test_tenant_and_product_setup(engine, cmdb, clear_cmdb):
    step_1_create_cmdb.run(cmdb, clear_cmdb)
    step_2_create_account_templates.run(cmdb, engine)
    step_3_create_segment_templates.run(cmdb, engine)
