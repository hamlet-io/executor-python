import os
import filecmp
import re
import json
import shutil
from . import utils
from hamlet.loggers import logging
from hamlet.backend.common.fsutils import Search


logger = logging.getLogger("CONTEXT_TREE")


def format_unit_cf_dir(base_dir, level, unit, placement, region):
    # Determine placement by region if not explicitly provided
    if not placement:
        if region == "us-east-1":
            placement = "global"
        else:
            placement = "default"
    return os.path.join(base_dir, unit, placement)


def parse_stack_filename(filename):
    # Parse file name for key values
    # Assume Account is part of the stack filename
    basename = os.path.basename(filename)
    pattern = (
        r"([a-z0-9]+)-(.+)-([1-9][0-9]{10})-([a-z]{2}-[a-z]+-[1-9])(-pseudo)?-(.+)"
    )
    match = re.match(pattern, basename)
    if match:
        return dict(
            stack_level=match.group(1),
            stack_deployment_unit=match.group(2),
            stack_account=match.group(3),
            stack_region=match.group(4),
        )
    pattern = r"([a-z0-9]+)-(.+-.+)-(.+)-([a-z]{2}-[a-z]+-[1-9])(-pseudo)?-(.+)"
    match = re.match(pattern, basename)
    if match:
        return dict(
            stack_level=match.group(1),
            stack_deployment_unit=match.group(2),
            stack_region=match.group(4),
            stack_account="",
        )
    pattern = r"([a-z0-9]+)-(.+)-([a-z]{2}-[a-z]+-[1-9])(-pseudo)?-(.+)"
    match = re.match(pattern, basename)
    if match:
        return dict(
            stack_level=match.group(1),
            stack_deployment_unit=match.group(2),
            stack_region=match.group(3),
            stack_account="",
        )
    return dict(
        stack_level="", stack_deployment_unit="", stack_region="", stack_account=""
    )


def find_gen3_root_dir(dirname):

    if os.environ.get("ROOT_DIR"):
        return os.environ.get("ROOT_DIR")

    marked_root_dir = Search.upwards(dirname, "root.json")
    if marked_root_dir is not None:
        return os.path.dirname(marked_root_dir)

    config_root_dir = os.path.dirname(Search.upwards(dirname, "config"))
    infrastructure_root_dir = os.path.dirname(Search.upwards(dirname, "infrastructure"))
    root_dir = config_root_dir or infrastructure_root_dir
    if Search.isdir(root_dir, "config") and Search.isdir(root_dir, "infrastructure"):
        return root_dir

    return None


def find_gen3_tenant_dir(root_dir, tenant):
    patterns = [
        os.path.join("**", tenant, "tenant.json"),
        os.path.join("**", tenant, "config", "tenant.json"),
        os.path.join("**", "tenant.json"),
    ]
    matches = Search.match_dirs(*patterns, root=root_dir, include_file_dirs=True)
    if not matches:
        raise Exception("Can't find tenant dir")
    return matches[0]


def find_gen3_account_dir(root_dir, account):
    patterns = [
        os.path.join("**", account, "account.json"),
        os.path.join("**", account, "config", "account.json"),
    ]
    matches = Search.match_dirs(*patterns, root=root_dir, include_file_dirs=True)
    if not matches:
        raise Exception("Can't find account dir")
    return matches[0]


def find_gen3_account_state_dir(root_dir, account):
    patterns = [
        os.path.join("**", account, "state"),
        os.path.join("**", "state", "**", account),
        os.path.join("**", "infrastructure", "**", account),
        os.path.join("**", account, "infrastructure"),
    ]
    matches = Search.match_dirs(*patterns, root=root_dir, include_file_dirs=True)
    if not matches:
        raise Exception("Can't find account infrastructure dir")
    return matches[0]


def find_gen3_product_dir(root_dir, product):
    patterns = [
        os.path.join("**", product, "product.json"),
        os.path.join("**", product, "config", "product.json"),
    ]
    matches = Search.match_dirs(*patterns, root=root_dir, include_file_dirs=True)
    if not matches:
        raise Exception("Can't find product dir")
    return matches[0]


def find_gen3_product_infrastructure_dir(root_dir, product):
    patterns = [
        os.path.join("**", "infrastructure", "**", product),
        os.path.join("**", product, "infrastructure"),
    ]
    matches = Search.match_dirs(*patterns, root=root_dir, include_file_dirs=True)
    if not matches:
        raise Exception("Can't find product infrastructure dir")
    return matches[0]


def find_gen3_environment_dir(root_dir, product, environment):
    product_dir = find_gen3_product_dir(root_dir, product)
    patterns = [os.path.join("**", "solutionsv2", environment, "environment.json")]
    matches = Search.match_dirs(*patterns, root=product_dir, include_file_dirs=True)
    if not matches:
        raise Exception("Can't find environment dir")
    return matches[0]


def get_gen3_env(environment_obj, name, prefix):
    return environment_obj[prefix + name]


def set_gen3_env_dir(environment_object, env, prefix, *directories):
    for directory in directories:
        if os.path.isdir(directory):
            environment_object[prefix + env] = directory
            return True
    return False


def find_gen3_dirs(
    environment_obj,
    root_dir,
    tenant="",
    account="",
    product="",
    environment="",
    segment="",
    prefix="",
):
    e = environment_obj  # shortcut
    tenant = tenant or e.TENANT
    account = account or e.ACCOUNT
    product = product or e.PRODUCT
    environment = environment or e.ENVIRONMENT
    segment = segment or e.SEGMENT

    set_gen3_env_dir(e, "ROOT_DIR", prefix, root_dir)
    set_gen3_env_dir(e, "TENANT_DIR", prefix, find_gen3_tenant_dir(root_dir, tenant))
    set_gen3_env_dir(e, "ACCOUNT_DIR", prefix, find_gen3_account_dir(root_dir, account))
    set_gen3_env_dir(
        e,
        "ACCOUNT_STATE_DIR",
        prefix,
        find_gen3_account_state_dir(root_dir, account),
    )
    e[prefix + "ACCOUNT_SETTINGS_DIR"] = os.path.join(
        get_gen3_env(e, "ACCOUNT_DIR", prefix), "settings"
    )
    e[prefix + "ACCOUNT_OPERATIONS_DIR"] = os.path.join(
        get_gen3_env(e, "ACCOUNT_STATE_DIR", prefix), "operations"
    )

    if product:
        set_gen3_env_dir(
            e, "PRODUCT_DIR", prefix, find_gen3_product_dir(root_dir, product)
        )
        set_gen3_env_dir(
            e,
            "PRODUCT_INFRASTRUCTURE_DIR",
            prefix,
            find_gen3_product_infrastructure_dir(root_dir, product),
        )
        e[prefix + "PRODUCT_SETTINGS_DIR"] = os.path.join(
            get_gen3_env(e, "PRODUCT_DIR", prefix), "settings"
        )
        e[prefix + "PRODUCT_SOLUTIONS_DIR"] = os.path.join(
            get_gen3_env(e, "PRODUCT_DIR", prefix), "solutionsv2"
        )
        e[prefix + "PRODUCT_OPERATIONS_DIR"] = os.path.join(
            get_gen3_env(e, "PRODUCT_INFRASTRUCTURE_DIR", prefix), "operations"
        )
        e[prefix + "PRODUCT_SHARED_SETTINGS_DIR"] = os.path.join(
            get_gen3_env(e, "PRODUCT_SETTINGS_DIR", prefix), "shared"
        )
        e[prefix + "PRODUCT_SHARED_SOLUTIONS_DIR"] = os.path.join(
            get_gen3_env(e, "PRODUCT_SOLUTIONS_DIR", prefix), "shared"
        )
        e[prefix + "PRODUCT_SHARED_OPERATIONS_DIR"] = os.path.join(
            get_gen3_env(e, "PRODUCT_OPERATIONS_DIR", prefix), "shared"
        )
        if environment:
            e[prefix + "ENVIRONMENT_SHARED_SETTINGS_DIR"] = os.path.join(
                get_gen3_env(e, "PRODUCT_SETTINGS_DIR", prefix), environment
            )
            e[prefix + "ENVIRONMENT_SHARED_SOLUTIONS_DIR"] = os.path.join(
                get_gen3_env(e, "PRODUCT_SOLUTIONS_DIR", prefix), environment
            )
            e[prefix + "ENVIRONMENT_SHARED_OPERATIONS_DIR"] = os.path.join(
                get_gen3_env(e, "PRODUCT_OPERATIONS_DIR", prefix), environment
            )
            if segment:
                e[prefix + "SEGMENT_SHARED_SETTINGS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_SETTINGS_DIR", prefix), "shared", segment
                )
                e[prefix + "SEGMENT_SHARED_SOLUTIONS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_SOLUTIONS_DIR", prefix), "shared", segment
                )
                e[prefix + "SEGMENT_SHARED_OPERATIONS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_OPERATIONS_DIR", prefix), "shared", segment
                )

                e[prefix + "SEGMENT_SETTINGS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_SETTINGS_DIR", prefix),
                    environment,
                    segment,
                )
                e[prefix + "SEGMENT_BUILDS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_SETTINGS_DIR", prefix),
                    environment,
                    segment,
                )
                e[prefix + "SEGMENT_SOLUTIONS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_SOLUTIONS_DIR", prefix),
                    environment,
                    segment,
                )
                e[prefix + "SEGMENT_OPERATIONS_DIR"] = os.path.join(
                    get_gen3_env(e, "PRODUCT_OPERATIONS_DIR", prefix),
                    environment,
                    segment,
                )


def upgrade_build_ref(root_dir, dry_run):
    legacy_files = Search.match_files(os.path.join("**", "build.ref"), root=root_dir)
    for legacy_file in legacy_files:
        logger.debug("Checking %s", legacy_file)
        upgraded_file = os.path.join(os.path.dirname(legacy_file), "build.json")
        if os.path.isfile(upgraded_file):
            continue
        logger.info("Upgrading %s", legacy_file)
        with open(legacy_file, "rt") as f:
            build_array = f.read().split(" ")
        try:
            build_data = {"Commit": build_array[0]}
        except IndexError as e:
            raise Exception(
                f"Unable to upgrade build reference in {legacy_file}"
            ) from e
        try:
            build_data["Tag"] = build_array[1]
        except IndexError:
            pass
        build_data["Formats"] = ["docker"]
        build_data = json.dumps(build_data, indent=4)
        if dry_run:
            logger.info(build_data)
            continue
        with open(upgraded_file, "wt+") as f:
            f.write(build_data)


def upgrade_shared_build_ref(root_dir, dry_run):
    legacy_files = Search.match_files(os.path.join("**", "*.ref"), root=root_dir)
    for legacy_file in legacy_files:
        if os.path.basename(legacy_file) == "build.ref":
            continue
        logger.debug("Checking %s", legacy_file)
        upgraded_file = os.path.join(os.path.dirname(legacy_file), "shared_build.json")
        if os.path.isfile(upgraded_file):
            continue
        logger.info("Upgrading %s", legacy_file)
        with open(legacy_file, "rt") as f:
            build_ref = f.read()
        upgraded_data = json.dumps({"Reference": build_ref}, indent=4)
        if dry_run:
            logger.info(upgraded_data)
            continue
        with open(upgraded_file, "wt+") as f:
            f.write(upgraded_data)


def upgrade_credentials(root_dir, dry_run):
    legacy_files = Search.match_files(
        os.path.join("**", "credentials.json"), root=root_dir
    )
    for legacy_file in legacy_files:
        logger.debug("Checking %s", legacy_file)
        with open(legacy_file, "rt") as f:
            legacy_data = json.load(f)
            credentials = legacy_data.get("Credentials")
            if credentials is None:
                return
        logger.info("Upgrading %s", legacy_file)
        upgraded_data = json.dumps(credentials or [], indent=4)
        if dry_run:
            logger.info(upgraded_data)
            continue
        with open(legacy_file, "wt+") as f:
            f.write(upgraded_data)


def upgrade_container_naming(root_dir, dry_run):
    legacy_files = Search.match_files(
        os.path.join("**", "container.json"), root=root_dir
    )
    for legacy_file in legacy_files:
        logger.debug("Checking %s", legacy_file)
        upgraded_file = os.path.join(os.path.dirname(legacy_file), "segment.json")
        if os.path.isfile(upgraded_file):
            continue
        logger.info("Upgrading %s", legacy_file)
        if dry_run:
            logger.info(f"{legacy_file}->{upgraded_file}")
            continue
        shutil.copy2(legacy_file, upgraded_file)


def upgrade_cmdb_repo_to_v1_0_0(root_dir, dry_run):
    # All build references now in json format
    upgrade_build_ref(root_dir, dry_run)
    # All shared build references now in json format
    upgrade_shared_build_ref(root_dir, dry_run)
    # Strip top level "Credentials" attribute from credentials
    upgrade_credentials(root_dir, dry_run)
    # Change of naming from "container" to "segment"
    upgrade_container_naming(root_dir, dry_run)
    return True


def cleanup_cmdb_repo_to_v1_0_0(root_dir, dry_run):
    # delete all .ref files. Because all of them converted into json format.
    legacy_files = Search.match_files(os.path.join("**", "*.ref"), root=root_dir)
    for legacy_file in legacy_files:
        logger.info("%sDeleting %s", dry_run, legacy_file)
        if dry_run:
            continue
        os.remove(legacy_file)
    # Change of naming from "container" to "segment"
    legacy_files = Search.match_files(
        os.path.join("**", "container.json"), root=root_dir
    )
    for legacy_file in legacy_files:
        logger.info("%sDeleting %s", dry_run, legacy_file)
        if dry_run:
            continue
        os.remove(legacy_file)
    return True


UPGRADE_V1_1_0_SOURCES = {
    "appsettings": "settings",
    "solutions": "solutionsv2",
    "credentials": "operations",
    "aws": "cf",
}


# Introduce separate environment and segment dirs
def upgrade_cmdb_repo_to_v1_1_0_settings(root_dir, dry_run, target_dir):
    # Create the shared file location for default segment
    shared_dir = os.path.join(target_dir, "shared")
    os.makedirs(shared_dir, exist_ok=True)
    sub_files = Search.list_files(root_dir)
    for sub_file in sub_files:
        src = os.path.join(root_dir, sub_file)
        dst = os.path.join(shared_dir, sub_file)
        logger.debug("Copying %s to %s", src, dst)
        if dry_run:
            continue
        shutil.copy2(src, dst)
    sub_dirs = Search.list_dirs(root_dir)
    for sub_dir in sub_dirs:
        environment = sub_dir
        sub_dir = os.path.join(root_dir, sub_dir)
        segment_dir = os.path.join(target_dir, environment, "default")
        os.makedirs(segment_dir, exist_ok=True)
        logger.debug("Copying %s to %s", sub_dir, segment_dir)
        if dry_run:
            continue
        for name in Search.list_all(sub_dir):
            src = os.path.join(sub_dir, name)
            dst = os.path.join(segment_dir, name)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        # Remove anything unwanted
        segment_files = Search.match_files(
            os.path.join("**", "*.ref"),
            os.path.join("**", "container.json"),
            root=segment_dir,
        )
        for segment_file in segment_files:
            logger.debug("Deleting %s", segment_file)
            os.remove(segment_file)
    return True


def upgrade_cmdb_repo_to_v1_1_0_state(root_dir, dry_run, target_dir):
    # Create the shared file location
    shared_dir = os.path.join(target_dir, "shared")
    os.makedirs(shared_dir, exist_ok=True)
    # Copy across the shared files
    cf_dir = os.path.join(root_dir, "cf")
    if os.path.isdir(cf_dir):
        sub_files = Search.list_files(cf_dir)
        for sub_file in sub_files:
            src = os.path.join(cf_dir, sub_file)
            dst = os.path.join(shared_dir, sub_file)
            logger.debug("Copying %s to %s", src, dst)
            if dry_run:
                continue
            shutil.copy2(src, dst)
    # Process each sub dir
    sub_dirs = Search.list_dirs(root_dir)
    for sub_dir in sub_dirs:
        if sub_dir == "cf":
            continue
        environment = sub_dir
        segment_dir = os.path.join(target_dir, environment, "default")
        cf_dir = os.path.join(root_dir, sub_dir, "cf")
        if not os.path.isdir(cf_dir):
            continue
        os.makedirs(segment_dir, exist_ok=True)
        logger.debug("Copying %s to %s", cf_dir, segment_dir)
        if dry_run:
            continue
        for name in Search.list_all(cf_dir):
            src = os.path.join(cf_dir, name)
            dst = os.path.join(segment_dir, name)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)


# config segment folders now under an environment folder
def upgrade_cmdb_repo_to_v1_1_0(root_dir, dry_run):
    for source in UPGRADE_V1_1_0_SOURCES:
        source_dirs = Search.match_dirs(os.path.join("**", source), root=root_dir)
        for source_dir in source_dirs:
            target_dir = os.path.join(
                os.path.dirname(source_dir), UPGRADE_V1_1_0_SOURCES[source]
            )
            logger.debug("Checking %s", source_dir)
            if os.path.isdir(target_dir):
                continue
            logger.info("Converting %s into %s", source_dir, target_dir)
            if source == "aws":
                upgrade_cmdb_repo_to_v1_1_0_state(source_dir, dry_run, target_dir)
            else:
                upgrade_cmdb_repo_to_v1_1_0_settings(source_dir, dry_run, target_dir)
            if dry_run:
                continue
            # Special processing
            if source == "solutions":
                # Shared solution files are specific to the default segment
                shared_default_dir = os.path.join(target_dir, "shared", "default")
                os.makedirs(shared_default_dir, exist_ok=True)
                target_shared_dir = os.path.join(target_dir, "shared")
                solution_files = Search.list_files(target_shared_dir)
                for solution_file in solution_files:
                    src = os.path.join(target_shared_dir, solution_file)
                    dst = os.path.join(shared_default_dir, solution_file)
                    logger.debug("Moving %s to %s", src, dst)
                    shutil.move(src, dst)
                # Process environments
                segment_files = Search.match_files(
                    os.path.join("**", "segment.json"), root=target_dir
                )
                for segment_file in segment_files:
                    segment_dir = os.path.dirname(segment_file)
                    environment_dir = os.path.dirname(segment_dir)
                    # Add environment.json file
                    with open(segment_file, "rt") as f:
                        segment = json.load(f)
                    environment_id = segment.get("Segment", {}).get("Environment")
                    environment_file = os.path.join(environment_dir, "environment.json")
                    logger.debug("Creating %s", environment_file)
                    with open(environment_file, "wt+") as f:
                        json.dump({"Environment": {"Id": environment_id}}, f)
                    logger.debug("Cleaning %s", segment_file)
                    segment_legacy_keys = ["Id", "Name", "Title", "Environment"]
                    for segment_legacy_key in segment_legacy_keys:
                        try:
                            del segment["Segment"][segment_legacy_key]
                        except KeyError:
                            pass
                    with open(segment_file, "wt") as f:
                        json.dump(segment, f)
                shared_segment_file = os.path.join(shared_default_dir, "segment.json")
                logger.debug("Creating %s", shared_segment_file)
                with open(shared_segment_file, "wt+") as f:
                    json.dump({"Segment": {"Id": "default"}}, f)
            elif source == "credentials":
                pem_files = Search.match_files(
                    os.path.join("**", "aws-ssh*.pem"), root=target_dir
                )
                for pem_file in pem_files:
                    filename = os.path.basename(pem_file)
                    segment_dir = os.path.dirname(pem_file)
                    # Move the pem files to make them invisible to the generation process
                    src = pem_file
                    dst = os.path.join(segment_dir, "." + filename)
                    logger.debug("Moving %s to %s", src, dst)
                    shutil.move(src, dst)
                    segment_ignore_file = os.path.join(segment_dir, ".gitignore")
                    if not os.path.isfile(segment_ignore_file):
                        logger.debug("Creaging %s", segment_ignore_file)
                        ignore_list = ["*.plaintext", "*.decrypted", "*.ppk"]
                        with open(segment_ignore_file, "wt+") as f:
                            f.write("\n".join(ignore_list))
    return True


def cleanup_cmdb_repo_to_v1_1_0(root_dir, dry_run):
    for source in UPGRADE_V1_1_0_SOURCES:
        source_dirs = Search.match_dirs(os.path.join("**", source), root=root_dir)
        for source_dir in source_dirs:
            target_dir = os.path.join(
                os.path.dirname(source_dir), UPGRADE_V1_1_0_SOURCES[source]
            )
            logger.debug("Checking %s", source_dir)
            logger.debug("Target dir %s", target_dir)
            if not os.path.isdir(target_dir):
                continue
            logger.info("%sDeleting %s", dry_run, source_dir)
            if dry_run:
                continue
            shutil.rmtree(source_dir)
    return True


def cleanup_cmdb_repo_to_v1_1_1(*args, **kwargs):
    # Rerun 1.1.0 to pick up errors in original implementation
    # Previously it only worked for product repos but now should
    # work for all repos
    return cleanup_cmdb_repo_to_v1_1_0(*args, **kwargs)


def cleanup_cmdb_repo_to_v2_0_0(root_dir, dry_run):
    config_dirs = Search.match_dirs(os.path.join("**", "config"), root=root_dir)
    for config_dir in config_dirs:
        solutions_dir = os.path.join(config_dir, "solutionsv2")
        if os.path.isdir(solutions_dir):
            logger.info("%sDeleting %s", dry_run, solutions_dir)
            if dry_run:
                continue
            shutil.rmtree(solutions_dir)
    return True


# container_* files now should be fragment_*
def upgrade_cmdb_repo_to_v1_2_0(root_dir, dry_run):
    legacy_files = Search.match_files(
        os.path.join("**", "container_*.ftl"), root=root_dir
    )
    for legacy_file in legacy_files:
        logger.debug("Checking %s", legacy_file)
        replacement_filename = os.path.basename(legacy_file).replace(
            "container_", "fragment_"
        )
        replacement_file = os.path.join(
            os.path.dirname(legacy_file), replacement_filename
        )
        if os.path.isfile(replacement_file):
            continue
        logger.info("%sRenaming %s to %s", dry_run, legacy_file, replacement_file)
        if dry_run:
            continue
        shutil.move(legacy_file, replacement_file)
    return True


def upgrade_cmdb_repo_to_v1_3_0(root_dir, dry_run):
    # Find accounts
    account_files = Search.match_files(
        os.path.join("**", "account.json"), root=root_dir
    )
    account_mappings = dict()
    for account_file in account_files:
        with open(account_file, "rt") as f:
            account = json.load(f)
            account_mappings[account["Account"]["AWSId"]] = account["Account"]["Id"]
    cf_dirs = Search.match_dirs(os.path.join("**", "cf"), root=root_dir)
    for cf_dir in cf_dirs:
        cmk_stacks = Search.match_files(
            os.path.join("**", "seg-cmk-*[0-9]-stack.json"), root=cf_dir
        )
        for cmk_stack in cmk_stacks:
            logger.info("Looking for CMK account in %s", cmk_stack)
            with open(cmk_stack, "rt") as f:
                cmk_stack_data = json.load(f)
            stack_outputs = cmk_stack_data["Stacks"][0]["Outputs"]
            cmk_account = None
            cmk_region = None
            for output in stack_outputs:
                if output["OutputKey"] == "Account":
                    cmk_account = output["OutputValue"]
                elif output["OutputKey"] == "Region":
                    cmk_region = output["OutputValue"]
            if cmk_account:
                cmk_account_id = account_mappings[cmk_account]
                cmk_path = os.path.dirname(cmk_stack)
                segment_stacks = Search.match_files(
                    os.path.join("**", "*stack.json"), root=cmk_path
                )
                for stack_file in segment_stacks:
                    parsed_stack = parse_stack_filename(stack_file)
                    stack_dir = os.path.dirname(stack_file)
                    stack_filename = os.path.basename(stack_file)
                    with open(stack_file, "rt") as f:
                        stack_data = json.load(f)
                    stack_outputs = stack_data["Stacks"][0]["Outputs"]
                    stackoutput_account = None
                    stackoutput_region = None
                    for output in stack_outputs:
                        if output["OutputKey"] == "Account":
                            stackoutput_account = output["OutputValue"]
                        elif output["OutputKey"] == "Region":
                            stackoutput_region = output["OutputValue"]
                    if not stackoutput_account:
                        logger.debug("Adding Account Output to %s", stack_file)
                        for stack in stack_data["Stacks"]:
                            stack["Outputs"].append(
                                {"OutputKey": "Account", "OutputValue": cmk_account}
                            )
                    if not stackoutput_region:
                        logger.debug("Adding Region Output to %s", stack_file)
                        for stack in stack_data["Stacks"]:
                            stack["Outputs"].append(
                                {
                                    "OutputKey": "Region",
                                    "OutputValue": parsed_stack["stack_region"],
                                }
                            )
                    if not stackoutput_region or not stackoutput_account:
                        with open(stack_file, "wt") as f:
                            json.dump(stack_data, f, indent=4)
                    if not parsed_stack["stack_account"]:
                        new_stack_file_name = os.path.basename(stack_file).replace(
                            f'-{parsed_stack["stack_region"]}-',
                            f'-{cmk_account_id}-{parsed_stack["stack_region"]}-',
                        )
                        if (
                            stack_filename != new_stack_file_name
                            and cmk_account_id not in stack_filename
                        ):
                            src = stack_file
                            dst = os.path.join(stack_dir, new_stack_file_name)
                            logger.debug("Moving %s to %s", src, dst)
                            if dry_run:
                                continue
                            shutil.move(src, dst)
                # Rename SSH keys to include Account/Region
                operations_path = cmk_path.replace(
                    os.path.join("infrastructure", "cf"),
                    os.path.join("infrastructure", "operations"),
                )
                logger.info("Checking for SSH Keys in %s", operations_path)
                pem_files = Search.match_files(
                    os.path.join("**", ".aws-ssh*.pem*"), root=operations_path
                )
                for pem_file in pem_files:
                    pem_dir = os.path.dirname(pem_file)
                    pem_basename = os.path.basename(pem_file)
                    new_basename = pem_basename.replace(
                        "aws-", f"aws-{cmk_account_id}-{cmk_region}-"
                    )
                    # Move the pem files to make them invisible to the generation process
                    src = pem_file
                    dst = os.path.join(pem_dir, new_basename)
                    logger.debug("Moving %s to %s", src, dst)
                    if dry_run:
                        continue
                    shutil.move(src, dst)
    return True


def upgrade_cmdb_repo_to_v1_3_1(root_dir, dry_run):
    # Find accounts
    account_files = Search.match_files(
        os.path.join("**", "account.json"), root=root_dir
    )
    account_mappings = dict()
    for account_file in account_files:
        with open(account_file, "rt") as f:
            account = json.load(f)
            account_mappings[account["Account"]["AWSId"]] = account["Account"]["Id"]
    cf_dirs = Search.match_dirs(os.path.join("**", "cf"), root=root_dir)
    for cf_dir in cf_dirs:
        cmk_stacks = Search.match_files(
            os.path.join("**", "seg-cmk-*[0-9]-stack.json"), root=cf_dir
        )
        for cmk_stack in cmk_stacks:
            logger.info("Looking for CMK account in %s", cmk_stack)
            with open(cmk_stack, "rt") as f:
                cmk_stack_data = json.load(f)
            stack_outputs = cmk_stack_data["Stacks"][0]["Outputs"]
            cmk_account = None
            for output in stack_outputs:
                if output["OutputKey"] == "Account":
                    cmk_account = output["OutputValue"]
            if cmk_account:
                cmk_account_id = account_mappings[cmk_account]
                cmk_path = os.path.dirname(cmk_stack)
                segment_cf = Search.match_files(os.path.join("**", "*"), root=cmk_path)
                for cf_file in segment_cf:
                    parsed_stack = parse_stack_filename(cf_file)
                    stack_dir = os.path.dirname(cf_file)
                    if not parsed_stack["stack_account"]:
                        cf_basename = os.path.basename(cf_file)
                        new_cf_basename = cf_basename.replace(
                            f'-{parsed_stack["stack_region"]}-',
                            f'-{cmk_account_id}-{parsed_stack["stack_region"]}-',
                        )
                        move_file = True
                        new_cf_file = os.path.join(stack_dir, new_cf_basename)
                        if (
                            cf_basename != new_cf_basename
                            and cmk_account_id not in cf_basename
                        ):
                            if os.path.isfile(new_cf_file):
                                if filecmp.cmp(cf_file, new_cf_file, False):
                                    move_file = False
                                else:
                                    logger.fatal(
                                        "Rename failed - %s already exists. Manual intervention necessary.",
                                        new_cf_file,
                                    )
                                    return False
                        if cf_file == new_cf_file:
                            logger.debug(
                                "Skipping %s, path is not changed", new_cf_file
                            )
                            continue
                        if move_file:
                            logger.debug("Moving %s to %s", cf_file, new_cf_file)
                        else:
                            logger.warn("%s already upgraded - removing", cf_file)
                        if dry_run:
                            continue
                        if move_file:
                            shutil.move(cf_file, new_cf_file)
                        else:
                            os.remove(cf_file)
    return True


def upgrade_cmdb_repo_to_v1_3_2(*args, **kwargs):
    # Rerun 1.3.1 to pick up errors in original implementation
    # Should be a no-op when run immediately after current 1.3.1
    # implementation
    return upgrade_cmdb_repo_to_v1_3_1(*args, **kwargs)


def upgrade_cmdb_repo_to_v2_0_0(root_dir, dry_run):
    # Reorganise cmdb to make it easier to manage via branches and dynamic cmdbs
    #
    # State is now in its own directory at the same level as config and infrastructure
    # Solutions is now under infrastructure
    # Builds are separated from settings and are now under infrastructure
    # Operations are now in their own directory at same level as config and
    # infrastructure. For consistency with config, a settings subdirectory has been
    # added.
    #
    # With this layout,
    # - infrastructure should be the same across environments assuming no builds
    #   are being promoted
    # - product and operations settings are managed consistently
    # - all the state info is cleanly separated (so potentially in its own repo)
    #
    # /config/settings
    # /operations/settings
    # /infrastructure/solutions
    # /infrastructure/builds
    # /state/cf
    # /state/cot
    #
    # If config and infrastructure are not in the one repo, then the upgrade must
    # be performed manually and the cmdb version manually updated
    config_dirs = Search.match_dirs(os.path.join("**", "config"), root=root_dir)
    for config_dir in config_dirs:
        base_dir = os.path.dirname(config_dir)
        solutions_dir = os.path.join(config_dir, "solutionsv2")
        settings_dir = os.path.join(config_dir, "settings")
        infrastructure_dir = os.path.join(base_dir, "infrastructure")
        state_dir = os.path.join(base_dir, "state")
        operations_dir = os.path.join(base_dir, "operations")
        state_subdirs = [
            os.path.join(infrastructure_dir, "cf"),
            os.path.join(infrastructure_dir, "cot"),
        ]
        if not os.path.isdir(infrastructure_dir):
            logger.warn(
                "%sUpdate to v2.0.0 for %s must be manually performed for split cmdb repos",
                dry_run,
                config_dir,
            )
            continue
        logger.debug("%sChecking %s", dry_run, base_dir)
        # Move the state into its own top level tree
        os.makedirs(base_dir, exist_ok=True)
        for state_subdir in state_subdirs:
            if os.path.isdir(state_subdir):
                src = state_subdir
                dst = os.path.join(state_dir, os.path.basename(state_subdir))
                logger.info("%sMoving %s to %s", dry_run, src, dst)
                if dry_run:
                    continue
                shutil.move(src, dst)
        # Move operations settings into their own top level tree
        orig_operations_settings_dir = os.path.join(infrastructure_dir, "operations")
        new_operation_settings_dir = os.path.join(operations_dir, "settings")
        if os.path.isdir(orig_operations_settings_dir):
            logger.info(
                "%sMoving %s to %s",
                dry_run,
                orig_operations_settings_dir,
                new_operation_settings_dir,
            )
            if dry_run:
                continue
            if not os.path.isdir(new_operation_settings_dir):
                os.makedirs(operations_dir, exist_ok=True)
                shutil.move(orig_operations_settings_dir, new_operation_settings_dir)
        # Copy the solutions tree from config to infrastructure and rename
        if os.path.isdir(solutions_dir):
            logger.info(
                "%sCopying %s to %s", dry_run, solutions_dir, infrastructure_dir
            )
            if not dry_run:
                # Leave existing solutions dir in place as it may be the current directory
                src = solutions_dir
                dst = os.path.join(infrastructure_dir, os.path.basename(src))
                shutil.copytree(src, dst)
            src = os.path.join(infrastructure_dir, "solutionsv2")
            dst = os.path.join(infrastructure_dir, "solutions")
            logger.info("%sRenaming %s to %s", dry_run, src, dst)
            if not dry_run:
                shutil.move(src, dst)
        # Copy the builds into their own tree
        builds_dir = os.path.join(infrastructure_dir, "builds")
        if not os.path.isdir(builds_dir):
            src = settings_dir
            dst = os.path.join(builds_dir, os.path.basename(src))
            logger.info("%sCopying %s to %s", dry_run, src, dst)
            if not dry_run:
                shutil.copytree(src, dst)
        # Remove the build files from the settings tree
        # Blob will pick up build references and shared builds
        logger.info("%sCleaning the settings tree", dry_run)
        setting_files = Search.match_files(
            os.path.join("**", "*build.json"), root=settings_dir
        )
        for setting_file in setting_files:
            logger.info("%sDeleting %s", dry_run, setting_file)
            if dry_run:
                continue
            os.remove(setting_file)
        # Build tree should only contain build references and shared builds
        logger.info("%sCleaning the builds tree", dry_run)
        if dry_run:
            build_files = Search.match_files(os.path.join("**", "*"), root=settings_dir)
        else:
            build_files = Search.match_files(os.path.join("**", "*"), root=builds_dir)
        build_files = [
            filename for filename in build_files if not filename.endswith("build.json")
        ]
        for build_file in build_files:
            logger.info("%sDeleting %s", dry_run, build_file)
            if dry_run:
                continue
            os.remove(build_file)

    return True


def upgrade_cmdb_repo_to_v2_0_1(root_dir, dry_run):
    # Reorganise state files into a directory tree based on deployment unit and placement
    #
    # The format of the state tree will follow the pattern
    # state/{df}/{env}/{seg}/{du}/{placement}
    #
    # Delete definition files because their file name contains the occurrence name not the
    # deployment unit. They will be regenerated into the correct dir on the next build.
    state_dirs = Search.match_dirs(os.path.join("**", "state"), root=root_dir)
    for state_dir in state_dirs:
        deployment_frameworks = Search.match_dirs("*", root=state_dir)
        for df_dir in deployment_frameworks:
            deployment_framework = os.path.basename(df_dir)
            logger.debug(
                "%sChecking %s deployment_framework", dry_run, deployment_framework
            )
            state_files = Search.match_files(os.path.join("**", "*"), root=df_dir)
            for state_file in state_files:
                state_basename = os.path.basename(state_file)
                state_dirname = os.path.dirname(state_file)
                stack_deployment_unit = ""
                # Filename format varies with deployment framework
                pattern_1 = r"([a-z0-9]+)-(.+)-([a-z][a-z0-9]+)-([a-z]{2}-[a-z]+-[1-9])(-pseudo)?-(.+)"
                pattern_2 = r"([a-z0-9]+)-(.+)-([a-z][a-z0-9]+)-(eastus|australiaeast|australiasoutheast|australiacentral|australiacentral2)(-pseudo)?-(.+)"  # noqa
                match = re.match(pattern_1, state_basename) or re.match(
                    pattern_2, state_basename
                )
                stack_level = ""
                stack_deployment_unit = ""
                stack_region = ""
                if match:
                    stack_level = match.group(1)
                    stack_deployment_unit = match.group(2)
                    stack_region = match.group(4)
                if not stack_deployment_unit:
                    # Legacy account formats
                    match = re.match(
                        r"account-([a-z][a-z0-9]+)-([a-z]{2}-[a-z]+-[1-9])-(.+)",
                        state_basename,
                    )
                    if match:
                        stack_level = "account"
                        stack_deployment_unit = match.group(1)
                        stack_region = match.group(2)
                    match = re.match(
                        r"account-([a-z]{2}-[a-z]+-[1-9])-(.+)", state_basename
                    )
                    if match:
                        stack_level = "account"
                        stack_deployment_unit = "s3"
                        stack_region = match.group(1)
                if not stack_deployment_unit:
                    # Legacy product formats
                    match = re.match(
                        r"product-([a-z]{2}-[a-z]+-[1-9])-(.+)", state_basename
                    )
                    if match:
                        stack_level = "product"
                        stack_deployment_unit = "cmk"
                        stack_region = match.group(1)
                if not stack_deployment_unit:
                    # Legacy segment formats
                    match = re.match(
                        r"seg-key-([a-z]{2}-[a-z]+-[1-9])-(.+)", state_basename
                    )
                    if match:
                        stack_level = "seg"
                        stack_deployment_unit = "cmk"
                        stack_region = match.group(1)
                    match = re.match(
                        r"cont-([a-z][a-z0-9]+)-([a-z]{2}-[a-z]+-[1-9])-(.+)",
                        state_basename,
                    )
                    if match:
                        stack_level = "seg"
                        stack_deployment_unit = match.group(1)
                        stack_region = match.group(2)
                if not stack_deployment_unit:
                    logger.warn(
                        "%sIgnoring %s, doesn't match one of the expected state filename formats",
                        dry_run,
                        state_basename,
                    )
                    continue
                if stack_level == "defn":
                    # Definition files are copied on every template creation
                    logger.info("%sDeleting %s", dry_run, state_file)
                    if dry_run:
                        continue
                    os.remove(state_file)
                else:
                    # Add deployment unit based subdirectories
                    if stack_deployment_unit in state_dirname:
                        logger.debug(
                            "%sIgnoring %s, already moved", dry_run, state_file
                        )
                    else:
                        du_dir = format_unit_cf_dir(
                            state_dirname,
                            stack_level,
                            stack_deployment_unit,
                            "",
                            stack_region,
                        )
                        src = state_file
                        dst = os.path.join(du_dir, state_basename)
                        logger.info("%sMoving %s to %s", dry_run, src, dst)
                        if dry_run:
                            continue
                        if not os.path.isdir(du_dir):
                            os.makedirs(du_dir, exist_ok=True)
                        shutil.move(src, dst)
    return True


GEN3_COMPATIBILITY = {}
# Entry example:  ["2.0.0"]=">=7.0.0"


def is_upgrade_compatible(cmdb_version, gen3_version):
    cmdb_version = utils.semver_clean(cmdb_version)
    compatible_range = GEN3_COMPATIBILITY.get(cmdb_version)
    if compatible_range:
        if not gen3_version:
            return "unknown"
        if not utils.semver_satisfies(gen3_version, compatible_range):
            return "incompatible"
    return "compatible"


def process_cmdb(root_dir, action, gen3_version, versions, dry_run):
    cmdb_git_repos = Search.match_dirs(os.path.join("**", "*.git"), root=root_dir)
    dry_run = "(Dryrun)" if dry_run else ""

    for cmdb_git_repo in cmdb_git_repos:

        cmdb_repo = os.path.dirname(cmdb_git_repo)
        cmdb_version_file = os.path.join(cmdb_repo, ".cmdb")
        current_version = ""
        pin_version = ""
        logger.debug("Checking repo %s", cmdb_repo)
        if os.path.isfile(cmdb_version_file):
            with open(cmdb_version_file, "rt") as f:
                cmdb_version_data = json.load(f)
            current_version = cmdb_version_data.get("Version", {}).get(
                action.capitalize()
            )
            pin_version = cmdb_version_data.get("Pin", {}).get(action.capitalize())
            logger.debug("Repo pinned at %s version %s", pin_version, current_version)
        else:
            with open(cmdb_version_file, "wt+") as f:
                json.dump({}, f)

        current_version = current_version or "v0.0.0"
        if utils.semver_compare(current_version, versions[-1]) >= 0:
            logger.debug(
                '%s of repo "%s" to %s is not required - skipping all version checks',
                action.capitalize(),
                cmdb_repo,
                versions[-1],
            )
            continue

        for version in versions:
            if utils.semver_compare(current_version, version) >= 0:
                logger.debug(
                    '%s of repo "%s" to %s is not required',
                    action.capitalize(),
                    cmdb_repo,
                    version,
                )
            else:
                logger.info(
                    '%s%s of repo "%s" to %s required ...',
                    dry_run,
                    action.capitalize(),
                    cmdb_repo,
                    version,
                )
            if pin_version:
                if utils.semver_compare(current_version, pin_version) < 0:
                    logger.warn(
                        '%s of repo "%s" to %s prevented by pin version %s',
                        action.capitalize(),
                        cmdb_repo,
                        version,
                        pin_version,
                    )
                    break
                else:
                    logger.debug(
                        '%s%s of repo "%s" to %s permitted by pin version %s',
                        dry_run,
                        action.capitalize(),
                    )
            compatibility = is_upgrade_compatible(version, gen3_version)
            if compatibility == "incompatible":
                logger.warn(
                    (
                        '%s%s of repo "%s" to %s is not compatible with the current gen3 framework version of %s. '
                        "Skipping upgrade process ..."
                    ),
                    dry_run,
                    action.capitalize(),
                    cmdb_repo,
                    version,
                    gen3_version,
                )
                break
            elif compatibility == "unknown":
                logger.warn(
                    (
                        '%s%s of repo "%" to %s requires the GEN3 framework version to be defined.'
                        "Skipping upgrade process ..."
                    ),
                    dry_run,
                    action.capitalize(),
                    cmdb_repo,
                    version,
                )
                break
            else:
                logger.debug(
                    '%s%s of repo "%s" to %s is compatible',
                    dry_run,
                    action.capitalize(),
                    cmdb_repo,
                    version,
                )

            cmdb_action_func = globals()[
                f'{action.lower()}_cmdb_repo_to_{version.replace(".", "_")}'
            ]
            if cmdb_action_func(cmdb_repo, dry_run):
                if dry_run:
                    logger.debug("%sSkipping later versions", dry_run)
                    break
                logger.info(
                    '%s of repo "%s" to %s successful',
                    action.capitalize(),
                    cmdb_repo,
                    version,
                )
                with open(cmdb_version_file, "rt") as f:
                    cmdb_version_data = json.load(f)
                utils.deep_dict_update(
                    cmdb_version_data, {"Version": {action.capitalize(): version}}
                )
                with open(cmdb_version_file, "wt") as f:
                    json.dump(cmdb_version_data, f)
                current_version = version

    return True


def upgrade_cmdb(root_dir, gen3_version, dry_run, maximum_version):
    maximum_version = maximum_version or "v1.3.2"
    upgrade_order = [
        "v1.0.0",
        "v1.1.0",
        "v1.2.0",
        "v1.3.0",
        "v1.3.1",
        "v1.3.2",
        "v2.0.0",
        "v2.0.1",
    ]
    logger.debug("Maximum CMDB upgrade version required is %s", maximum_version)
    required_versions = utils.semver_upgrade_list(upgrade_order, maximum_version)
    logger.debug("Required CMDB upgrade order is %s", required_versions)

    return process_cmdb(root_dir, "upgrade", gen3_version, required_versions, dry_run)


def cleanup_cmdb(root_dir, gen3_version, dry_run, maximum_version):
    maximum_version = maximum_version or "v1.1.1"
    upgrade_order = ["v1.0.0", "v1.1.0", "v1.1.1", "v2.0.0"]
    logger.debug("Maximum CMDB cleanup version required is %s", maximum_version)
    required_versions = utils.semver_upgrade_list(upgrade_order, maximum_version)
    logger.debug("Required CMDB cleanup order is %s", required_versions)

    return process_cmdb(root_dir, "cleanup", gen3_version, required_versions, dry_run)
