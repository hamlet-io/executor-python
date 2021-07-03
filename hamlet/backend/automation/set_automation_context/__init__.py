from hamlet.backend.common import runner


def run(
    release_mode=None,
    deployment_mode=None,
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
        'AUTOMATION_LOG_LEVEL': log_level,
        **env
    }
    opts = {
        '-t': tenant,
        '-a': account,
        '-p': product,
        '-e': environment,
        '-s': segment,
        '-d': deployment_mode,
        '-r': release_mode
    }
    runner.run('setContext.sh', [], opts, env, _is_cli, script_base_path_env='AUTOMATION_BASE_DIR')
