import os
import json
import tempfile
from unittest import mock

# import subprocess
from hamlet.backend.generate.cmdb import account, tenant, product
from hamlet.backend.create.template.environment import Environment
from hamlet.backend.create.template import context_tree as ct
from .conftest import conf


def test_find_gen3_dirs(clear_cmdb, cmdb):
    clear_cmdb()

    tenant_name = conf["cmdb"]["tenant"]["tenant_name"]
    account_name = conf["cmdb"]["account"]["account_name"]
    product_name = conf["cmdb"]["product"]["product_name"]
    segment_name = conf["cmdb"]["product"]["segment_name"]
    environment_name = conf["cmdb"]["product"]["environment_name"]

    with mock.patch.dict(os.environ, {"ROOT_DIR": cmdb.ROOT_DIR}):

        with cmdb() as path:
            tenant.run(**conf["cmdb"]["tenant"], output_dir=path())
        with cmdb("accounts") as path:
            account.run(**conf["cmdb"]["account"], output_dir=path())
        with cmdb() as path:
            product.run(**conf["cmdb"]["product"], output_dir=path())

        with cmdb() as path:
            root_dir = path()
            assert root_dir == ct.find_gen3_root_dir(path())
            tenant_dir = os.path.join(root_dir, "accounts", tenant_name)
            assert tenant_dir == ct.find_gen3_tenant_dir(root_dir, tenant_name)
            account_base_dir = os.path.join(root_dir, "accounts", account_name)
            account_dir = os.path.join(account_base_dir, "config")
            account_state_dir = os.path.join(account_base_dir, "infrastructure")
            assert account_dir == ct.find_gen3_account_dir(root_dir, account_name)
            assert account_state_dir == ct.find_gen3_account_state_dir(
                root_dir, account_name
            )
            product_base_dir = os.path.join(root_dir, product_name)
            product_dir = os.path.join(product_base_dir, "config")
            product_infr_dir = os.path.join(product_base_dir, "infrastructure")
            environment_dir = os.path.join(product_dir, "solutionsv2", environment_name)
            assert product_dir == ct.find_gen3_product_dir(root_dir, product_name)
            assert product_infr_dir == ct.find_gen3_product_infrastructure_dir(
                root_dir, product_name
            )
            assert environment_dir == ct.find_gen3_environment_dir(
                root_dir, product_name, environment_name
            )
            e = Environment()
            ct.find_gen3_dirs(
                e,
                root_dir,
                tenant=tenant_name,
                account=account_name,
                product=product_name,
                environment=environment_name,
                segment=segment_name,
            )
            assert e.ROOT_DIR == root_dir
            assert e.TENANT_DIR == tenant_dir

            assert e.ACCOUNT_DIR == account_dir
            assert e.ACCOUNT_STATE_DIR == account_state_dir
            assert e.ACCOUNT_SETTINGS_DIR == os.path.join(account_dir, "settings")
            assert e.ACCOUNT_OPERATIONS_DIR == os.path.join(
                account_state_dir, "operations"
            )
            product_settings_dir = os.path.join(product_dir, "settings")
            product_operations_dir = os.path.join(product_infr_dir, "operations")
            product_solutions_dir = os.path.join(product_dir, "solutionsv2")
            environment_shared_operations_dir = os.path.join(
                product_infr_dir, "operations", environment_name
            )
            environment_shared_settings_dir = os.path.join(
                product_dir, "settings", environment_name
            )
            environment_shared_solutions_dir = os.path.join(
                product_dir, "solutionsv2", environment_name
            )
            segment_solutions_dir = os.path.join(
                product_dir, "solutionsv2", environment_name, segment_name
            )
            segment_settings_dir = os.path.join(
                product_dir, "settings", environment_name, segment_name
            )
            segment_operations_dir = os.path.join(
                product_infr_dir, "operations", environment_name, segment_name
            )
            segment_builds_dir = segment_settings_dir
            segment_shared_settings_dir = os.path.join(
                product_dir, "settings", "shared", segment_name
            )
            segment_shared_solutions_dir = os.path.join(
                product_dir, "solutionsv2", "shared", segment_name
            )
            segment_shared_operations_dir = os.path.join(
                product_infr_dir, "operations", "shared", segment_name
            )
            assert e.PRODUCT_DIR == product_dir
            assert e.PRODUCT_SETTINGS_DIR == product_settings_dir
            assert e.PRODUCT_INFRASTRUCTURE_DIR == product_infr_dir
            assert e.PRODUCT_OPERATIONS_DIR == product_operations_dir
            assert e.PRODUCT_SOLUTIONS_DIR == product_solutions_dir
            assert e.PRODUCT_SHARED_SETTINGS_DIR == os.path.join(
                product_settings_dir, "shared"
            )
            assert e.PRODUCT_SHARED_OPERATIONS_DIR == os.path.join(
                product_operations_dir, "shared"
            )
            assert e.PRODUCT_SHARED_SOLUTIONS_DIR == os.path.join(
                product_solutions_dir, "shared"
            )
            assert e.ENVIRONMENT_SHARED_SETTINGS_DIR == environment_shared_settings_dir
            assert (
                e.ENVIRONMENT_SHARED_SOLUTIONS_DIR == environment_shared_solutions_dir
            )
            assert (
                e.ENVIRONMENT_SHARED_OPERATIONS_DIR == environment_shared_operations_dir
            )
            assert e.SEGMENT_SOLUTIONS_DIR == segment_solutions_dir
            assert e.SEGMENT_SETTINGS_DIR == segment_settings_dir
            assert e.SEGMENT_OPERATIONS_DIR == segment_operations_dir
            assert e.SEGMENT_BUILDS_DIR == segment_builds_dir
            assert e.SEGMENT_SHARED_SETTINGS_DIR == segment_shared_settings_dir
            assert e.SEGMENT_SHARED_SOLUTIONS_DIR == segment_shared_solutions_dir
            assert e.SEGMENT_SHARED_OPERATIONS_DIR == segment_shared_operations_dir
            print(e)


class FSNode:
    def __init__(self, path):
        self.path = path

    def __getitem__(self, key):
        return self.__class__(os.path.join(self.path, key))

    def __setitem__(self, key, value):
        if not isinstance(value, str):
            value = json.dumps(value, indent=4)
        os.makedirs(self.path, exist_ok=True)
        with open(os.path.join(self.path, key), "wt+") as f:
            f.write(value)

    def exists(self):
        return os.path.exists(self.path)

    def mkdir(self):
        os.makedirs(self.path, exist_ok=True)
        return self

    def touchfile(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        open(self.path, "w").close()
        return self

    def mkfile(self, data):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wt+") as f:
            f.write(data)
        return self

    def mkjson(self, data):
        data = json.dumps(data)
        self.mkfile(data)
        return self

    def isfile(self):
        return os.path.isfile(self.path)

    def isdir(self):
        return os.path.isdir(self.path)

    def json(self):
        if self.isfile():
            with open(self.path, "rt") as f:
                return json.load(f)
        raise TypeError(f"{self.path} is not a file")

    def text(self):
        if self.isfile():
            with open(self.path, "rt") as f:
                return f.read()
        raise TypeError(f"{self.path} is not a file")


def test_upgrade_version_1_0_0():
    def create_test_fs(root):
        root = FSNode(root)

        root["build.ref"] = "commit1 tag1"
        root["builds"]["build.ref"] = "commit2 tag2"

        root["shared-build.ref"] = "reference1"
        root["shared-builds"]["shared-build.ref"] = "reference2"

        root["credentials.json"] = {"Credentials": ["1", "2"]}
        root["credentials"]["credentials.json"] = {"Credentials": ["3", "4"]}

        root["container.json"] = {"Id": "1"}
        root["containers"]["container.json"] = {"Id": "2"}

    def assert_post_upgrade_structure(root):
        root = FSNode(root)
        # Legacy
        assert not root["build.ref"].exists()
        assert not root["builds"]["build.ref"].exists()

        assert not root["shared-build.ref"].exists()
        assert not root["shared-builds"]["shared-build.ref"].exists()

        assert not root["container.json"].exists()
        assert not root["containers"]["container.json"].exists()
        # Upgraded
        assert root["build.json"].json() == {
            "Commit": "commit1",
            "Tag": "tag1",
            "Formats": ["docker"],
        }
        assert root["builds"]["build.json"].json() == {
            "Commit": "commit2",
            "Tag": "tag2",
            "Formats": ["docker"],
        }

        assert root["shared_build.json"].json() == {"Reference": "reference1"}
        assert root["shared-builds"]["shared_build.json"].json() == {
            "Reference": "reference2"
        }

        assert root["credentials.json"].json() == ["1", "2"]
        assert root["credentials"]["credentials.json"].json() == ["3", "4"]

        assert root["segment.json"].json() == {"Id": "1"}
        assert root["containers"]["segment.json"].json() == {"Id": "2"}

    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        assert ct.upgrade_cmdb_repo_to_v1_0_0(root, "")
        assert ct.cleanup_cmdb_repo_to_v1_0_0(root, "")
        assert_post_upgrade_structure(root)


def test_upgrade_version_1_1_0():
    def create_test_fs(root):
        root = FSNode(root)

        appsettings = root["appsettings"]
        appsettings["appsettings-file.json"].touchfile()
        appsettings["appsettings-env"]["subdir"][
            "appsettings-env-sub-file.json"
        ].touchfile()
        appsettings["appsettings-env"]["appsettings-env-file.json"].touchfile()

        solutions = root["solutions"]
        solutions["solutions-file.json"].touchfile()
        solutions["segment.json"] = {
            "Segment": {
                "Environment": "solutions",
                "Id": "Id",
                "Name": "Name",
                "Title": "Title",
                "NonLegacyKey": "NonLegacyKey",
            }
        }
        solutions["solutions-env"]["subdir"]["solutions-env-sub-file.json"].touchfile()
        solutions["solutions-env"]["solutions-env-file.json"].touchfile()
        solutions["solutions-env"]["segment.json"] = {
            "Segment": {
                "Environment": "solutions-env",
                "Id": "Id",
                "Name": "Name",
                "Title": "Title",
                "NonLegacyKey": "NonLegacyKey",
            }
        }

        credentials = root["credentials"]
        credentials["credentials-file.json"].touchfile()
        credentials["aws-ssh.pem"].touchfile()
        credentials["credentials-env"]["subdir"][
            "credentials-env-sub-file.json"
        ].touchfile()
        credentials["credentials-env"]["credentials-env-file.json"].touchfile()
        credentials["credentials-env"][".gitignore"] = "test"
        credentials["credentials-env"]["aws-ssh-env.pem"].touchfile()

        aws = root["aws"]
        aws["aws-file.json"].touchfile()
        aws["cf"]["aws-cf-file.json"].touchfile()
        aws["aws-env"]["subdir"]["aws-env-sub-file.json"].touchfile()
        aws["aws-env"]["cf"]["aws-env-cf-file.json"].touchfile()
        aws["aws-env"]["cf"]["subdir"]["aws-env-cf-sub-file.json"].touchfile()

    def assert_post_upgrade_structure(root):
        root = FSNode(root)
        # Legacy
        assert not root["appsettings"].exists()
        # Upgraded
        settings = root["settings"]
        assert settings["shared"]["appsettings-file.json"].isfile()
        assert settings["appsettings-env"]["default"]["subdir"][
            "appsettings-env-sub-file.json"
        ].isfile()
        assert settings["appsettings-env"]["default"][
            "appsettings-env-file.json"
        ].isfile()
        # Legacy
        assert not root["solutions"].exists()
        # Upgraded
        solutionsv2 = root["solutionsv2"]
        assert solutionsv2.isdir()
        assert solutionsv2["shared"]["default"]["solutions-file.json"].isfile()
        assert solutionsv2["shared"]["default"]["segment.json"].json() == {
            "Segment": {"Id": "default"}
        }
        assert solutionsv2["solutions-env"]["default"]["subdir"][
            "solutions-env-sub-file.json"
        ].isfile()
        assert solutionsv2["solutions-env"]["default"][
            "solutions-env-file.json"
        ].isfile()
        assert solutionsv2["solutions-env"]["default"]["segment.json"].json() == {
            "Segment": {"NonLegacyKey": "NonLegacyKey"}
        }
        assert solutionsv2["solutions-env"]["environment.json"].json() == {
            "Environment": {"Id": "solutions-env"}
        }
        # Legacy
        assert not root["credentials"].exists()
        # Upgraded
        operations = root["operations"]
        assert operations["shared"][".aws-ssh.pem"].isfile()
        assert operations["shared"][".gitignore"].text() == "\n".join(
            ["*.plaintext", "*.decrypted", "*.ppk"]
        )
        assert operations["shared"]["credentials-file.json"].isfile()
        assert operations["credentials-env"]["default"]["subdir"][
            "credentials-env-sub-file.json"
        ].isfile()
        assert operations["credentials-env"]["default"][
            "credentials-env-file.json"
        ].isfile()
        assert operations["credentials-env"]["default"][".aws-ssh-env.pem"].isfile()
        assert operations["credentials-env"]["default"][".gitignore"].text() == "test"
        # Legacy
        assert not root["aws"].exists()
        # Upgraded
        cf = root["cf"]
        assert not cf["shared"]["aws-file.json"].isfile()
        assert cf["shared"]["aws-cf-file.json"].isfile()
        assert cf["aws-env"]["default"]["aws-env-cf-file.json"].isfile()
        assert cf["aws-env"]["default"]["subdir"]["aws-env-cf-sub-file.json"].isfile()
        assert not cf["aws-env"]["default"]["aws-env-sub-file.json"].exists()

    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        # subprocess.call('tree -a', shell=True, cwd=tmp_dir)
        assert ct.upgrade_cmdb_repo_to_v1_1_0(root, "")
        assert ct.cleanup_cmdb_repo_to_v1_1_0(root, "")
        # subprocess.call('tree -a', shell=True, cwd=tmp_dir)
        assert_post_upgrade_structure(root)


def test_upgrade_version_1_2_0():
    def create_test_fs(root):
        root = FSNode(root)
        root["container_template.ftl"] = "container_template"
        root["container_blueprint.ftl"] = "container_blueprint"
        root["container_exists.ftl"] = "container_exists"
        root["fragment_exists.ftl"] = "fragment_exists"

        sub_dir = root["sub_dir"]
        sub_dir["container_template.ftl"] = "container_template"
        sub_dir["container_blueprint.ftl"] = "container_blueprint"
        sub_dir["container_exists.ftl"] = "container_exists"
        sub_dir["fragment_exists.ftl"] = "fragment_exists"

    def assert_post_upgrade_structure(root):
        root = FSNode(root)
        assert not root["container_template.ftl"].exists()
        assert not root["container_blueprint.ftl"].exists()
        assert root["container_exists.ftl"].text() == "container_exists"
        assert root["fragment_exists.ftl"].text() == "fragment_exists"

        sub_dir = root["sub_dir"]
        assert not sub_dir["container_template.ftl"].exists()
        assert not sub_dir["container_blueprint.ftl"].exists()
        assert sub_dir["container_exists.ftl"].text() == "container_exists"
        assert sub_dir["fragment_exists.ftl"].text() == "fragment_exists"

    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        assert ct.upgrade_cmdb_repo_to_v1_2_0(root, "")
        assert_post_upgrade_structure(root)


def test_upgrade_version_1_3_0():
    CMK_STACK_DATA = {
        "Stacks": [
            {
                "Outputs": [
                    {"OutputKey": "Account", "OutputValue": "AWSId_1"},
                    {"OutputKey": "Region", "OutputValue": "AWS_Region_1"},
                ]
            }
        ]
    }

    EMPTY_STACK_DATA = {
        "Stacks": [{"Outputs": [{"OutputKey": "Custom", "OutputValue": "Custom"}]}]
    }

    UPDATED_EMPTY_STACK_DATA = {
        "Stacks": [
            {
                "Outputs": [
                    {"OutputKey": "Custom", "OutputValue": "Custom"},
                    {"OutputKey": "Account", "OutputValue": "AWSId_1"},
                    {"OutputKey": "Region", "OutputValue": "us-east-1"},
                ]
            }
        ]
    }

    def create_test_fs(root):
        root = FSNode(root)

        accounts = root["accounts"]
        accounts["account"]["config"]["account.json"] = {
            "Account": {"Id": "Id_1", "AWSId": "AWSId_1"}
        }
        cf = root["infrastructure"]["cf"]
        operations = root["infrastructure"]["operations"]

        cf["seg-cmk-1-stack.json"] = CMK_STACK_DATA
        cf[
            "stacklevel-deplymentunit-10000000000-us-east-1-stack.json"
        ] = EMPTY_STACK_DATA
        cf["stacklevel-deplyment-unit-xxxx-us-east-1-stack.json"] = EMPTY_STACK_DATA
        cf["stacklevel-deplymentunit-us-east-1-stack.json"] = EMPTY_STACK_DATA

        operations[".aws-ssh-0.pem"] = "0"
        operations[".aws-ssh-1.pem"] = "1"

    def assert_post_upgrade_structure(root):
        root = FSNode(root)

        cf = root["infrastructure"]["cf"]
        operations = root["infrastructure"]["operations"]

        assert cf["seg-cmk-1-stack.json"].json() == CMK_STACK_DATA

        assert not cf["stacklevel-deplyment-unit-xxxx-us-east-1-stack.json"].exists()
        assert not cf["stacklevel-deplymentunit-us-east-1-stack.json"].exists()

        assert (
            cf["stacklevel-deplymentunit-10000000000-us-east-1-stack.json"].json()
            == UPDATED_EMPTY_STACK_DATA
        )
        assert (
            cf["stacklevel-deplyment-unit-xxxx-Id_1-us-east-1-stack.json"].json()
            == UPDATED_EMPTY_STACK_DATA
        )
        assert (
            cf["stacklevel-deplymentunit-Id_1-us-east-1-stack.json"].json()
            == UPDATED_EMPTY_STACK_DATA
        )

        assert not operations[".aws-ssh-0.pem"].exists()
        assert not operations[".aws-ssh-1.pem"].exists()

        assert operations[".aws-Id_1-AWS_Region_1-ssh-0.pem"].text() == "0"
        assert operations[".aws-Id_1-AWS_Region_1-ssh-1.pem"].text() == "1"

    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        assert ct.upgrade_cmdb_repo_to_v1_3_0(root, "")
        assert_post_upgrade_structure(root)


def test_upgrade_version_1_3_1():
    import subprocess

    CMK_STACK_DATA = {
        "Stacks": [
            {
                "Outputs": [
                    {"OutputKey": "Account", "OutputValue": "AWSId_1"},
                    {"OutputKey": "Region", "OutputValue": "AWS_Region_1"},
                ]
            }
        ]
    }

    ACCOUNT_DATA = {"Account": {"Id": "10000000000", "AWSId": "AWSId_1"}}

    def create_test_fs(root):
        root = FSNode(root)

        accounts = root["accounts"]
        accounts["account"]["config"]["account.json"] = ACCOUNT_DATA
        cf = root["infrastructure"]["cf"]

        cf["seg-cmk-1-stack.json"] = CMK_STACK_DATA
        cf["stacklevel-deplymentunit-10000000001-us-east-1-stack.json"] = "1"
        cf["stacklevel-deplyment-unit-xxxx-us-east-1-stack.json"] = "2"
        cf["stacklevel-deplymentunit-us-east-1-stack.json"] = "3"

    def assert_post_upgrade_structure(root):
        root = FSNode(root)

        cf = root["infrastructure"]["cf"]

        assert cf["seg-cmk-1-stack.json"].json() == CMK_STACK_DATA
        assert (
            cf["stacklevel-deplymentunit-10000000001-us-east-1-stack.json"].text()
            == "1"
        )
        assert not cf["stacklevel-deplyment-unit-xxxx-us-east-1-stack.json"].exists()
        assert not cf["stacklevel-deplymentunit-us-east-1-stack.json"].exists()

        assert (
            cf["stacklevel-deplyment-unit-xxxx-10000000000-us-east-1-stack.json"].text()
            == "2"
        )
        assert (
            cf["stacklevel-deplymentunit-10000000000-us-east-1-stack.json"].text()
            == "3"
        )

    # Regular run without exceptional cases
    with tempfile.TemporaryDirectory() as root:
        create_test_fs(root)
        subprocess.call("tree -a", shell=True, cwd=root)
        assert ct.upgrade_cmdb_repo_to_v1_3_1(root, "")
        subprocess.call("tree -a", shell=True, cwd=root)
        assert_post_upgrade_structure(root)

    # Exceptional cases:
    # Files content is different, manual intervention required
    with tempfile.TemporaryDirectory() as root_dir:
        root = FSNode(root_dir)

        cf = root["infrastructure"]["cf"]
        accounts = root["accounts"]
        accounts["account"]["config"]["account.json"] = ACCOUNT_DATA
        cf["seg-cmk-1-stack.json"] = CMK_STACK_DATA
        cf["stacklevel-deplymentunit-us-east-1-stack.json"] = "1"
        cf["stacklevel-deplymentunit-10000000000-us-east-1-stack.json"] = "2"

        assert not ct.upgrade_cmdb_repo_to_v1_3_1(root_dir, "")

        assert cf["stacklevel-deplymentunit-us-east-1-stack.json"].text() == "1"
        assert (
            cf["stacklevel-deplymentunit-10000000000-us-east-1-stack.json"].text()
            == "2"
        )

    # Files content is equal, removing legacy file
    with tempfile.TemporaryDirectory() as root_dir:
        root = FSNode(root_dir)

        cf = root["infrastructure"]["cf"]
        accounts = root["accounts"]
        accounts["account"]["config"]["account.json"] = ACCOUNT_DATA
        cf["seg-cmk-1-stack.json"] = CMK_STACK_DATA
        cf["stacklevel-deplymentunit-us-east-1-stack.json"] = "1"
        cf["stacklevel-deplymentunit-10000000000-us-east-1-stack.json"] = "1"

        assert ct.upgrade_cmdb_repo_to_v1_3_1(root_dir, "")

        assert not cf["stacklevel-deplymentunit-us-east-1-stack.json"].exists()
        assert (
            cf["stacklevel-deplymentunit-10000000000-us-east-1-stack.json"].text()
            == "1"
        )


def test_upgrade_version_2_0_0():
    with tempfile.TemporaryDirectory() as root:
        root = FSNode(root)

        product = root["product"]
        config = product["config"].mkdir()
        config["config.json"].touchfile()
        settings = config["settings"].mkdir()
        settings["build.json"].touchfile()
        settings["shared-build.json"].touchfile()
        settings["not-a-build-file.json"].touchfile()
        solutionsv2 = config["solutionsv2"].mkdir()
        solutionsv2["solution.json"].touchfile()
        infrastructure = product["infrastructure"].mkdir()
        infrastructure_cf = infrastructure["cf"].mkdir()
        infrastructure_cf["cf.json"].touchfile()
        infrastructure_cot = infrastructure["cot"].mkdir()
        infrastructure_cot["cot.json"].touchfile()
        infrastructure_operations = infrastructure["operations"].mkdir()
        infrastructure_operations["infrastructure-operations.json"].touchfile()
        state = product["state"].mkdir()
        state["state.json"].touchfile()
        operations = product["operations"].mkdir()
        operations["operations.json"].touchfile()

        assert ct.upgrade_cmdb_repo_to_v2_0_0(root.path, "")
        assert ct.cleanup_cmdb_repo_to_v2_0_0(root.path, "")

        assert config["config.json"].isfile()
        assert not config["solutionsv2"].exists()
        assert settings["not-a-build-file.json"].isfile()
        assert not settings["build.json"].exists()
        assert not settings["shared-build.json"].exists()

        assert not infrastructure_operations.exists()
        assert not infrastructure_cf.exists()
        assert not infrastructure_cot.exists()

        assert infrastructure["builds"]["settings"]["build.json"].isfile()
        assert infrastructure["builds"]["settings"]["shared-build.json"].isfile()

        assert infrastructure["solutions"]["solution.json"].isfile()

        assert state["cot"]["cot.json"].isfile()
        assert state["cf"]["cf.json"].isfile()

        assert operations["operations.json"].isfile()
        assert operations["settings"]["infrastructure-operations.json"].isfile()


def test_upgrade_version_2_0_1():
    with tempfile.TemporaryDirectory() as root:
        root = FSNode(root)
        state = root["state"].mkdir()
        cf = state["cf"].mkdir()

        cf["level-deploymentunit-aa-us-east-1-suffix.json"].touchfile()
        # definition file should be removed
        cf["defn-deploymentunit-aa-eastus-suffix.json"].touchfile()
        # level account
        cf["account-deploymentunit-us-east-2-suffix.json"].touchfile()
        # level acccount dunit s3
        cf["account-us-east-1-suffix.json"].touchfile()
        # level product dunit cmk
        cf["product-us-east-1-suffix.json"].touchfile()
        # level seg dunit cmk
        cf["seg-key-us-east-1-suffix.json"].touchfile()
        # level seg
        cf["cont-deploymentunit-us-east-1-suffix.json"].touchfile()
        # already moved
        # level product dunit cmk
        cf["cmk"]["default"]["product-us-east-9-suffix.json"].touchfile()
        assert ct.upgrade_cmdb_repo_to_v2_0_1(root.path, "")

        assert not cf["defn-deploymentunit-aa-eastus-suffix.json"].exists()
        # global if region == 'us-east-1' otherwise default
        cmk = cf["cmk"]
        assert cmk["global"]["product-us-east-1-suffix.json"].isfile()
        assert cmk["global"]["seg-key-us-east-1-suffix.json"].isfile()

        deploymentunit = cf["deploymentunit"]
        assert deploymentunit["default"][
            "account-deploymentunit-us-east-2-suffix.json"
        ].isfile()
        assert deploymentunit["global"][
            "cont-deploymentunit-us-east-1-suffix.json"
        ].isfile()
        assert deploymentunit["global"][
            "level-deploymentunit-aa-us-east-1-suffix.json"
        ].isfile()

        s3 = cf["s3"]
        assert s3["global"]["account-us-east-1-suffix.json"].isfile()

        assert cf["cmk"]["default"]["product-us-east-9-suffix.json"].isfile()


# pretty basic test, just to check that there are no critical errors
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v1_0_0")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v1_1_0")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v1_2_0")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v1_3_0")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v1_3_1")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v1_3_2")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v2_0_0")
@mock.patch("hamlet.backend.create.template.context_tree.upgrade_cmdb_repo_to_v2_0_1")
@mock.patch("hamlet.backend.create.template.context_tree.cleanup_cmdb_repo_to_v1_0_0")
@mock.patch("hamlet.backend.create.template.context_tree.cleanup_cmdb_repo_to_v1_1_0")
@mock.patch("hamlet.backend.create.template.context_tree.cleanup_cmdb_repo_to_v1_1_1")
@mock.patch("hamlet.backend.create.template.context_tree.cleanup_cmdb_repo_to_v2_0_0")
def test_upgrade_cmdb(
    cleanup_cmdb_repo_to_v2_0_0,
    cleanup_cmdb_repo_to_v1_1_1,
    cleanup_cmdb_repo_to_v1_1_0,
    cleanup_cmdb_repo_to_v1_0_0,
    upgrade_cmdb_repo_to_v2_0_1,
    upgrade_cmdb_repo_to_v2_0_0,
    upgrade_cmdb_repo_to_v1_3_2,
    upgrade_cmdb_repo_to_v1_3_1,
    upgrade_cmdb_repo_to_v1_3_0,
    upgrade_cmdb_repo_to_v1_2_0,
    upgrade_cmdb_repo_to_v1_1_0,
    upgrade_cmdb_repo_to_v1_0_0,
):

    with tempfile.TemporaryDirectory() as root:
        root = FSNode(root)
        root[".git"].mkdir()
        ct.upgrade_cmdb(root.path, "", "", "v2.0.1")
        ct.cleanup_cmdb(root.path, "", "", "v2.0.0")
        assert root[".cmdb"].json() == {
            "Version": {"Upgrade": "v2.0.1", "Cleanup": "v2.0.0"}
        }

    cleanup_cmdb_repo_to_v2_0_0.assert_called_once()
    cleanup_cmdb_repo_to_v1_1_1.assert_called_once()
    cleanup_cmdb_repo_to_v1_1_0.assert_called_once()
    cleanup_cmdb_repo_to_v1_0_0.assert_called_once()

    upgrade_cmdb_repo_to_v2_0_1.assert_called_once()
    upgrade_cmdb_repo_to_v2_0_0.assert_called_once()
    upgrade_cmdb_repo_to_v1_3_2.assert_called_once()
    upgrade_cmdb_repo_to_v1_3_1.assert_called_once()
    upgrade_cmdb_repo_to_v1_3_0.assert_called_once()
    upgrade_cmdb_repo_to_v1_2_0.assert_called_once()
    upgrade_cmdb_repo_to_v1_1_0.assert_called_once()
    upgrade_cmdb_repo_to_v1_0_0.assert_called_once()
