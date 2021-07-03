from hamlet.backend.common import runner


def run(
    function_id=None,
    deployment_unit=None,
    input_payload=None,
    include_log_tail=None,
    log_level=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
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
        "ROOT_DIR": root_dir,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run("runLambda.sh", [], options, env, _is_cli)
