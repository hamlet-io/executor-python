from hamlet.backend.common import runner


def run(
    deployment_group=None,
    deployment_unit=None,
    build_logs=None,
    node_package_manager=None,
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
        "-l": build_logs,
        "-n": node_package_manager,
        "-o": binary_output_dir,
        "-u": deployment_unit,
        "-g": deployment_group,
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
