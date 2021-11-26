import os
import json
import tempfile
import pytest
from hamlet.backend.common.context import (
    Context,
    NoLevelFileError,
    NoRootFileError,
    NoTenantFoundError,
    NoAccountsFoundError,
    MultipleTenantsFoundError,
    MultipleAccountsFoundError,
    SpecifiedAccountNotFoundError,
    AccountLevel,
    TenantLevel,
    ProductLevel,
    EnvironmentLevel,
    SegmentLevel,
)


def test_context_basics():
    with tempfile.TemporaryDirectory() as temp_dir:

        def cmdb(*paths):
            return os.path.join(temp_dir, "cmdb", *paths)

        # setting fake cmdb
        os.mkdir(cmdb())
        open(cmdb("root.json"), "w").close()
        os.makedirs(cmdb("accounts"))
        os.makedirs(cmdb("accounts", "tenant"))
        os.makedirs(cmdb("accounts", "tenant-second"))
        os.makedirs(cmdb("accounts", "account-name-1", "config"))
        os.makedirs(cmdb("accounts", "account-name-2", "config"))
        open(cmdb("accounts", "tenant", "tenant.json"), "w").close()
        open(cmdb("accounts", "tenant-second", "tenant.json"), "w").close()
        os.makedirs(cmdb("product", "config"))
        os.makedirs(cmdb("product", "config", "solutions", "environment"))
        os.makedirs(cmdb("product", "config", "solutions", "environment", "segment"))
        with open(
            cmdb("product", "config", "solutions", "environment", "environment.json"),
            "wt+",
        ) as f:
            json.dump({"Name": "environment_name"}, f)
        with open(
            cmdb(
                "product",
                "config",
                "solutions",
                "environment",
                "segment",
                "segment.json",
            ),
            "wt+",
        ) as f:
            json.dump({"Name": "segment_name"}, f)
        with open(cmdb("product", "config", "product.json"), "wt+") as f:
            json.dump({"Name": "product_name"}, f)
        with open(
            cmdb("accounts", "account-name-1", "config", "account.json"), "wt+"
        ) as f:
            json.dump({"Name": "account-name-1"}, f)
        with open(
            cmdb("accounts", "account-name-2", "config", "account.json"), "wt+"
        ) as f:
            json.dump({"Name": "account-name-2"}, f)

        context = Context(cmdb())
        assert context.root_dir == cmdb()

        with pytest.raises(NoRootFileError):
            Context(temp_dir)

        with pytest.raises(MultipleTenantsFoundError):
            AccountLevel(cmdb("accounts", "account-name-1"))

        os.remove(cmdb("accounts", "tenant-second", "tenant.json"))
        account_level = AccountLevel(cmdb("accounts", "account-name-1"))
        assert account_level.props["Name"] == "account-name-1"
        assert account_level.tenant_dir == cmdb("accounts", "tenant")
        assert account_level.level_file_path == cmdb(
            "accounts", "account-name-1", "config", "account.json"
        )

        tenant_level = TenantLevel(cmdb("accounts", "tenant"))
        assert tenant_level.level_file_path == cmdb("accounts", "tenant", "tenant.json")

        with pytest.raises(NoLevelFileError):
            ProductLevel(
                cmdb("accounts", "account-name-1"),
                config=dict(account="account-name-1"),
            )

        with pytest.raises(MultipleAccountsFoundError):
            ProductLevel(cmdb("product"))

        product_level = ProductLevel(
            cmdb("product"), config=dict(account="account-name-1")
        )
        assert product_level.tenant_dir == cmdb("accounts", "tenant")
        assert product_level.account_dir == cmdb("accounts", "account-name-1")

        product_level = ProductLevel(
            cmdb("product"), config=dict(account="account-name-2")
        )
        assert product_level.tenant_dir == cmdb("accounts", "tenant")
        assert product_level.account_dir == cmdb("accounts", "account-name-2")

        with pytest.raises(SpecifiedAccountNotFoundError):
            ProductLevel(cmdb("product"), config=dict(account="account-name-3"))

        environment_level = EnvironmentLevel(
            cmdb("product", "config", "solutions", "environment"),
            config=dict(account="account-name-1"),
        )
        assert environment_level.tenant_dir == cmdb("accounts", "tenant")
        assert environment_level.account_dir == cmdb("accounts", "account-name-1")
        assert environment_level.props["Environment"] == "environment"

        segment_level = SegmentLevel(
            cmdb("product", "config", "solutions", "environment", "segment"),
            config=dict(account="account-name-2"),
        )
        assert segment_level.tenant_dir == cmdb("accounts", "tenant")
        assert segment_level.account_dir == cmdb("accounts", "account-name-2")
        assert segment_level.props["Environment"] == "environment"
        assert segment_level.props["Segment"] == "segment"

        os.remove(cmdb("accounts", "account-name-1", "config", "account.json"))

        product_level = ProductLevel(
            cmdb("product"), config=dict(account="account-name-2")
        )
        assert product_level.tenant_dir == cmdb("accounts", "tenant")
        assert product_level.account_dir == cmdb("accounts", "account-name-2")

        with pytest.raises(SpecifiedAccountNotFoundError):
            ProductLevel(cmdb("product"), config=dict(account="account-name-1"))

        product_level = ProductLevel(cmdb("product"))
        assert product_level.tenant_dir == cmdb("accounts", "tenant")
        assert product_level.account_dir == cmdb("accounts", "account-name-2")

        os.remove(cmdb("accounts", "account-name-2", "config", "account.json"))

        with pytest.raises(NoAccountsFoundError):
            ProductLevel(cmdb("product"))

        os.remove(cmdb("accounts", "tenant", "tenant.json"))
        with pytest.raises(NoTenantFoundError):
            ProductLevel(cmdb("product"))
