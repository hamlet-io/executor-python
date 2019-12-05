# from . import step_1_create_cmdb
# from . import step_2_create_account_templates
# from . import step_3_create_soultion_templates
from . import step_1_create_cmdb


def test(cmdb, clear_cmdb):
    step_1_create_cmdb.test_cmdb_creation(cmdb, clear_cmdb)
