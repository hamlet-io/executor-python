from hamlet.backend.common import runner


def run(
    deployment_unit=None,
    deployment_group=None,
    sentry_source_map_s3_url=None,
    sentry_url_prefix=None,
    sentry_release_name=None,
    app_type=None,
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
        "-m": sentry_source_map_s3_url,
        "-p": sentry_url_prefix,
        "-r": sentry_release_name,
        "-u": deployment_unit,
        "-g": deployment_group,
        "-a": app_type,
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
        "runSentryRelease.sh",
        args=[],
        options=options,
        engine=engine,
        env=env,
        _is_cli=_is_cli,
    )
