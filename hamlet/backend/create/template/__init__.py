from hamlet.backend.common import runner


def run(
    entrance=None,
    config_ref=None,
    resource_group=None,
    request_ref=None,
    region=None,
    deployment_group=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    deployment_mode=None,
    generation_provider=None,
    generation_framework=None,
    generation_input_source=None,
    output_dir=None,
    disable_output_cleanup=None,
    entrance_parameter=None,
    log_level=None,
    log_format=None,
    root_dir=None,
    tenant=None,
    district_type=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    engine=None,
    _is_cli=False,
    **kwargs,
):
    if isinstance(entrance_parameter, dict):
        entrance_parameter = tuple([f"{k}={v}" for k, v in entrance_parameter.items()])

    options = {
        "-e": entrance,
        "-c": config_ref,
        "-g": resource_group,
        "-l": deployment_group,
        "-q": request_ref,
        "-r": region,
        "-u": deployment_unit,
        "-z": deployment_unit_subset,
        "-d": deployment_mode,
        "-p": generation_provider,
        "-f": generation_framework,
        "-i": generation_input_source,
        "-o": output_dir,
        "-x": disable_output_cleanup,
        "-y": entrance_parameter,
    }
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "GENERATION_LOG_FORMAT": log_format,
        "ROOT_DIR": root_dir,
        "DISTRICT_TYPE": district_type,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run(
        "createTemplate.sh",
        args=[],
        options=options,
        env=env,
        engine=engine,
        _is_cli=_is_cli,
    )
