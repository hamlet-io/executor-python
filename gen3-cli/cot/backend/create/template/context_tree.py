import os
from cot.loggers import logging
from cot.backend.common.fsutils import Search


logger = logging.getLogger('CONTEXT_TREE')


def find_gen3_root_dir(dirname):
    marked_root_dir = Search.upwards(dirname, 'root.json')
    if marked_root_dir is not None:
        return os.path.dirname(marked_root_dir)
    config_root_dir = os.path.dirname(Search.upwards(dirname, 'config'))
    infrastructure_root_dir = os.path.dirname(Search.upwards(dirname, 'infrastructure'))
    root_dir = config_root_dir or infrastructure_root_dir
    if Search.isdir(root_dir, 'config') and Search.isdir(root_dir, 'infrastructure'):
        return root_dir
    return None


def find_gen3_tenant_dir(root_dir, tenant):
    patterns = [
        os.path.join('**', tenant, 'tenant.json'),
        os.path.join('**', tenant, 'config', 'tenant.json'),
        os.path.join('**', 'tenant.json')
    ]
    matches = Search.match_dirs(
        *patterns,
        root=root_dir
    )
    if not matches:
        raise Exception("Can't find tenant dir")
    return matches[0]


def find_gen3_account_dir(root_dir, account):
    patterns = [
        os.path.join('**', account, 'account.json'),
        os.path.join('**', account, 'config', 'account.json')
    ]
    matches = Search.match_dirs(
        *patterns,
        root=root_dir
    )
    if not matches:
        raise Exception("Can't find account dir")
    return matches[0]


def find_gen3_account_infrastructure_dir(root_dir, account):
    patterns = [
        os.path.join('**', 'infrastructure', '**', account),
        os.path.join('**', account, 'infrastructure')
    ]
    matches = Search.match_dirs(
        *patterns,
        root=root_dir
    )
    if not matches:
        raise Exception("Can't find account infrastructure dir")
    return matches[0]


def find_gen3_product_dir(root_dir, product):
    patterns = [
        os.path.join('**', product, 'product.json'),
        os.path.join('**', product, 'config', 'product.json')
    ]
    matches = Search.match_dirs(
        *patterns,
        root=root_dir
    )
    if not matches:
        raise Exception("Can't find product dir")
    return matches[0]


def find_gen3_product_infrastructure_dir(root_dir, product):
    patterns = [
        os.path.join('**', 'infrastructure', '**', product),
        os.path.join('**', product, 'infrastructure'),
    ]
    matches = Search.match_dirs(
        *patterns,
        root=root_dir
    )
    if not matches:
        raise Exception("Can't find product infrastructure dir")
    return matches[0]


def find_gen3_environment_dir(root_dir, product, environment):
    product_dir = find_gen3_product_dir(root_dir, product)
    patterns = [
        os.path.join('**', 'solutionsv2', environment, 'environment.json')
    ]
    matches = Search.match_dirs(
        *patterns,
        root=product_dir
    )
    if not matches:
        raise Exception("Can't find environment dir")
    return matches[0]


def get_gen3_env(environment_obj, name, prefix):
    return environment_obj[prefix + name]


def set_gen3_env_dir(
    environment_object,
    env,
    prefix,
    *directories
):
    for directory in directories:
        if os.path.isdir(directory):
            environment_object[prefix + env] = directory
            return True
    return False


def find_gen3_dirs(
    environment_obj,
    root_dir,
    tenant='',
    account='',
    product='',
    environment='',
    segment='',
    prefix=''
):
    e = environment_obj  # shortcut
    tenant = tenant or e.TENANT
    account = account or e.ACCOUNT
    product = product or e.PRODUCT
    environment = environment or e.ENVIRONMENT
    segment = segment or e.SEGMENT

    set_gen3_env_dir(e, 'ROOT_DIR', prefix, root_dir)
    set_gen3_env_dir(e, 'TENANT_DIR', prefix, find_gen3_tenant_dir(root_dir, tenant))
    set_gen3_env_dir(e, 'ACCOUNT_DIR', prefix, find_gen3_account_dir(root_dir, account))
    set_gen3_env_dir(e, 'ACCOUNT_INFRASTRUCTURE_DIR', prefix, find_gen3_account_infrastructure_dir(root_dir, account))
    e[prefix + 'ACCOUNT_SETTINGS_DIR'] = os.path.join(
        get_gen3_env(e, 'ACCOUNT_DIR', prefix),
        'settings'
    )
    e[prefix + 'ACCOUNT_OPERATIONS_DIR'] = os.path.join(
        get_gen3_env(e, 'ACCOUNT_INFRASTRUCTURE_DIR', prefix),
        'operations'
    )

    if product:
        set_gen3_env_dir(e, 'PRODUCT_DIR', prefix, find_gen3_product_dir(root_dir, product))
        set_gen3_env_dir(
            e,
            'PRODUCT_INFRASTRUCTURE_DIR',
            prefix,
            find_gen3_product_infrastructure_dir(root_dir, product)
        )
        e[prefix + 'PRODUCT_SETTINGS_DIR'] = os.path.join(
            get_gen3_env(e, 'PRODUCT_DIR', prefix),
            'settings'
        )
        e[prefix + 'PRODUCT_SOLUTIONS_DIR'] = os.path.join(
            get_gen3_env(e, 'PRODUCT_DIR', prefix),
            'solutionsv2'
        )
        e[prefix + 'PRODUCT_OPERATIONS_DIR'] = os.path.join(
            get_gen3_env(e, 'PRODUCT_INFRASTRUCTURE_DIR', prefix),
            'operations'
        )
        e[prefix + 'PRODUCT_SHARED_SETTINGS_DIR'] = os.path.join(
            get_gen3_env(e, 'PRODUCT_SETTINGS_DIR', prefix),
            'shared'
        )
        e[prefix + 'PRODUCT_SHARED_SOLUTIONS_DIR'] = os.path.join(
            get_gen3_env(e, 'PRODUCT_SOLUTIONS_DIR', prefix),
            'shared'
        )
        e[prefix + 'PRODUCT_SHARED_OPERATIONS_DIR'] = os.path.join(
            get_gen3_env(e, 'PRODUCT_OPERATIONS_DIR', prefix),
            'shared'
        )
        if environment:
            e[prefix + 'ENVIRONMENT_SHARED_SETTINGS_DIR'] = os.path.join(
                get_gen3_env(e, 'PRODUCT_SETTINGS_DIR', prefix),
                environment
            )
            e[prefix + 'ENVIRONMENT_SHARED_SOLUTIONS_DIR'] = os.path.join(
                get_gen3_env(e, 'PRODUCT_SOLUTIONS_DIR', prefix),
                environment
            )
            e[prefix + 'ENVIRONMENT_SHARED_OPERATIONS_DIR'] = os.path.join(
                get_gen3_env(e, 'PRODUCT_OPERATIONS_DIR', prefix),
                environment
            )
            if segment:
                e[prefix + 'SEGMENT_SHARED_SETTINGS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_SETTINGS_DIR', prefix),
                    'shared',
                    segment
                )
                e[prefix + 'SEGMENT_SHARED_SOLUTIONS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_SOLUTIONS_DIR', prefix),
                    'shared',
                    segment
                )
                e[prefix + 'SEGMENT_SHARED_OPERATIONS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_OPERATIONS_DIR', prefix),
                    'shared',
                    segment
                )

                e[prefix + 'SEGMENT_SETTINGS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_SETTINGS_DIR', prefix),
                    environment,
                    segment
                )
                e[prefix + 'SEGMENT_BUILDS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_SETTINGS_DIR', prefix),
                    environment,
                    segment
                )
                e[prefix + 'SEGMENT_SOLUTIONS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_SOLUTIONS_DIR', prefix),
                    environment,
                    segment
                )
                e[prefix + 'SEGMENT_OPERATIONS_DIR'] = os.path.join(
                    get_gen3_env(e, 'PRODUCT_OPERATIONS_DIR', prefix),
                    environment,
                    segment
                )
