from hamlet.backend.common import runner


def run(
    log_level=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
    **kwargs,
):
    env = {
        'GENERATION_LOG_LEVEL': log_level,
        'ROOT_DIR': root_dir,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment
        **kwargs
    }
    runner.run('execution/setContext.sh', [], {}, env, _is_cli, script_base_path_env='GENERATION_BASE_DIR')
