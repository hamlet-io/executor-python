from hamlet.backend.common import runner


def run(
    deployment_unit=None,
    run_setup=None,
    force_binary_build=None,
    submit_binary=None,
    binary_build_process=None,
    build_logs=None,
    environment_badge=None,
    environment_badge_content=None,
    node_package_manager=None,
    app_version_source=None,
    binary_output_dir=None,
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
        "-b": binary_build_process,
        "-d": environment_badge_content,
        "-e": environment_badge,
        "-f": force_binary_build,
        "-l": build_logs,
        "-m": submit_binary,
        "-n": node_package_manager,
        "-o": binary_output_dir,
        "-s": run_setup,
        "-u": deployment_unit,
        "-v": app_version_source,
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
        "runExpoAppPublish.sh",
        args=[],
        options=options,
        engine=engine,
        env=env,
        _is_cli=_is_cli,
    )
