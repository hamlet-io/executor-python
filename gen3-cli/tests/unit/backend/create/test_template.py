from cot.backend.create import template as create_template_backend


def test_account(cmdb):
    with cmdb('accounts'):
        pass


def test_product(cmdb):
    with cmdb('test_product_id'):
        pass
