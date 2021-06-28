from hamlet.backend.common import runner


def run(
    exclude_account_dirs=None,
    product_config_reference=None,
    product_infrastructure_reference=None,
    exclude_product_dirs=None,
    account_config_reference=None,
    account_infrastructure_reference=None,
    env=None,
    log_level=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
    **kwargs,
):
    opts={
        '-a': exclude_account_dirs,
        '-c': product_config_reference,
        '-i': product_infrastructure_reference,
        '-r': exclude_product_dirs,
        '-x': account_config_reference,
        '-y': account_infrastructure_reference,
    }
    env = {
        'AUTOMATION_LOG_LEVEL': log_level,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment,
        **env
    }
    runner.run('constructTree.sh', [], opts, env, _is_cli, script_base_path_env='AUTOMATION_BASE_DIR')
