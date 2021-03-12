from hamlet.backend.common import runner


def run(
    delete=None,
    stack_initiate=None,
    stack_monitor=None,
    stack_wait=None,
    stack_name=None,
    deployment_group=None,
    region=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    output_dir=None,
    dryrun=None,
    log_level=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
    **kwargs,
):
    options = {
        '-d': delete,
        '-i': stack_initiate,
        '-m': stack_monitor,
        '-o': output_dir,
        '-w': stack_wait,
        '-n': stack_name,
        '-r': region,
        '-y': dryrun,
        '-u': deployment_unit,
        '-z': deployment_unit_subset,
        '-l': deployment_group
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
    runner.run('manageStack.sh', [], options, env, _is_cli)
