from hamlet.backend.common import runner


def run(
    function_id=None,
    deployment_unit=None,
    input_payload=None,
    include_log_tail=None,
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
        "-f": function_id,
        "-u": deployment_unit,
        "-i": input_payload,
        "-l": include_log_tail,
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
        "runLambda.sh",
        args=[],
        options=options,
        engine=engine,
        env=env,
        _is_cli=_is_cli,
    )
