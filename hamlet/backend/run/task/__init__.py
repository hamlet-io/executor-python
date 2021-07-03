from hamlet.backend.common import runner


def run(
    container_id=None,
    delay=None,
    env_name=None,
    component=None,
    component_instance=None,
    component_version=None,
    tier=None,
    value=None,
    task=None,
    instance=None,
    version=None,
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
        "-c": container_id,
        "-d": delay,
        "-e": env_name,
        "-i": component,
        "-j": component_instance,
        "-k": component_version,
        "-t": tier,
        "-v": value,
        "-w": task,
        "-x": instance,
        "-y": version,
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
    runner.run("runTask.sh", [], options, env, _is_cli)
