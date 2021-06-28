from hamlet.backend.common import runner


def run(
    deployment_units=None,
    release_mode=None,
    release_tag=None,
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
        'DEPLOYMENT_UNIT_LIST' : deployment_units,
        'RELEASE_MODE' : release_mode,
        'RELEASE_TAG' : release_tag,
        'AUTOMATION_LOG_LEVEL': log_level,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment,
        **env
    }

    runner.run('acceptRelease.sh', [], {}, env, _is_cli, script_base_path_env='AUTOMATION_DIR')
