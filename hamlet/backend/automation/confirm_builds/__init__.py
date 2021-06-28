from hamlet.backend.common import runner


def run(
    release_mode=None,
    acceptance_tag=None,
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
    env = {
        'RELEASE_MODE' : release_mode,
        'ACCEPTANCE_TAG' : acceptance_tag,
        'AUTOMATION_LOG_LEVEL': log_level,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment,
        **env
    }
    runner.run('confirmBuilds.sh', [], {}, env, _is_cli, script_base_path_env='AUTOMATION_DIR')
