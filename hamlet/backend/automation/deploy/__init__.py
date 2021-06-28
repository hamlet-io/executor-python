from hamlet.backend.common import runner


def run(
    deployment_units=None,
    automation_job_identifier=None,
    product_config_commit=None,
    product_infrastructure_reference=None,
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
    env = {
        'DEPLOYMENT_UNIT_LIST': deployment_units,
        'AUTOMATION_JOB_IDENTIFIER': automation_job_identifier,
        'PRODUCT_CONFIG_COMMIT': product_config_commit,
        'PRODUCT_INFRASTRUCTURE_REFERENCE': product_infrastructure_reference,
        'AUTOMATION_LOG_LEVEL': log_level,
        'TENANT': tenant,
        'ACCOUNT': account,
        'PRODUCT': product,
        'ENVIRONMENT': environment,
        'SEGMENT': segment,
        **env
    }
    runner.run('deploy.sh', [], {}, env, _is_cli, script_base_path_env='AUTOMATION_DIR')
