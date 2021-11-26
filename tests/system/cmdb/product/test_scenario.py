from . import step_1_install_engine
from . import step_2_create_cmdb
from . import step_3_create_account_templates
from . import step_4_create_segment_templates


def test_tenant_and_product_setup(engine, clear_engine, cmdb, clear_cmdb):
    step_1_install_engine.run(engine, clear_engine)
    step_2_create_cmdb.run(cmdb, clear_cmdb)
    step_3_create_account_templates.run(cmdb, engine)
    step_4_create_segment_templates.run(cmdb, engine)
