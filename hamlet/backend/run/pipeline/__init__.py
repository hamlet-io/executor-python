from hamlet.backend.common import runner


def run(
    component=None,
    tier=None,
    instance=None,
    version=None,
    pipeline_status_only=None,
    pipeline_allow_concurrent=None,
    log_level=None,
    log_format=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    engine=None,
    _is_cli=False,
    **kwargs
):
    options = {
        "-i": component,
        "-t": tier,
        "-x": instance,
        "-y": version,
        "-s": pipeline_status_only,
        "-c": pipeline_allow_concurrent,
    }
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "GENERATION_LOG_FORMAT": log_format,
        "ROOT_DIR": root_dir,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run(
        "runPipeline.sh",
        args=[],
        options=options,
        engine=engine,
        env=env,
        _is_cli=_is_cli,
    )
