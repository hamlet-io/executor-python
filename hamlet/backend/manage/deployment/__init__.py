from hamlet.backend.common import runner


def run(
    delete=None,
    deployment_initiate=None,
    deployment_group=None,
    deployment_monitor=None,
    region=None,
    deployment_scope=None,
    deployment_unit=None,
    deployment_wait=None,
    deployment_unit_subset=None,
    output_dir=None,
    dryrun=None,
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
    **kwargs,
):
    options = {
        "-d": delete,
        "-i": deployment_initiate,
        "-m": deployment_monitor,
        "-l": deployment_group,
        "-r": region,
        "-s": deployment_scope,
        "-u": deployment_unit,
        "-w": deployment_wait,
        "-y": dryrun,
        "-z": deployment_unit_subset,
        "-o": output_dir,
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
        "manageDeployment.sh",
        args=[],
        options=options,
        env=env,
        engine=engine,
        _is_cli=_is_cli,
    )
