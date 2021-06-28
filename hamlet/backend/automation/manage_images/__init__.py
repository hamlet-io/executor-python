from hamlet.backend.common import runner


def run(
    registry_scope=None,
    dockerfile=None,
    docker_context=None,
    image_formats=None,
    code_commit=None,
    image_paths=None,
    docker_image=None,
    deployment_unit=None,
    env=None,
    log_level=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
    **kwargs,
):

    opts = {
        '-c': registry_scope,
        '-d': dockerfile,
        '-e': docker_context,
        '-f': image_formats,
        '-g': code_commit,
        '-i': image_paths,
        '-t': docker_image,
        '-u': deployment_unit,
    }

    env = {
        'AUTOMATION_LOG_LEVEL': log_level,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment,
        **env
    }
    runner.run('manageImages.sh', [], opts, env, _is_cli, script_base_path_env='AUTOMATION_DIR')
