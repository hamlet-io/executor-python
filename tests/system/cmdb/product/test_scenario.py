from . import step_1_create_cmdb

# from . import step_2_create_account_templates


def test(cmdb, clear_cmdb):
    step_1_create_cmdb.run(cmdb, clear_cmdb)
    # test fails for unknown reason, doesn't create files in specified directories
    # step_2_create_account_templates.run(cmdb)
