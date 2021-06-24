from hamlet.backend.common import runner


def run(
    deployment_unit=None,
    run_setup=None,
    binary_expiration=None,
    force_binary_build=None,
    submit_binary=None,
    disable_ota=None,
    binary_build_process=None,
    qr_build_formats=None,
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
        '-u': deployment_unit,
        '-s': run_setup,
        '-t': binary_expiration,
        '-f': force_binary_build,
        '-m': submit_binary,
        '-o': disable_ota,
        '-b': binary_build_process,
        '-q': qr_build_formats
    }
    env = {
        'GENERATION_LOG_LEVEL': log_level,
        'ROOT_DIR': root_dir,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment,
    }
    runner.run('runExpoAppPublish.sh', [], options, env, _is_cli)
