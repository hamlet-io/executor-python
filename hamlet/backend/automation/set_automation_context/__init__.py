from hamlet.backend.common import runner


def run(
    release_mode=None,
    deployment_mode=None,
    log_level=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    context_credentials=None,
    engine=None,
    _is_cli=False,
    env={},
):
    env = {
        "AUTOMATION_LOG_LEVEL": log_level,
        "AUTOMATION_CONTEXT_CREDENTIALS": context_credentials,
        **env,
    }
    opts = {
        "-t": tenant,
        "-a": account,
        "-p": product,
        "-e": environment,
        "-s": segment,
        "-d": deployment_mode,
        "-r": release_mode,
    }
    runner.run(
        "setContext.sh",
        args=[],
        options=opts,
        env=env,
        engine=engine,
        _is_cli=_is_cli,
        script_base_path_env="AUTOMATION_BASE_DIR",
    )
