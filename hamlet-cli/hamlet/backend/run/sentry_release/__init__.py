from hamlet.backend.common import runner


def run(
    sentry_source_map_s3_url=None,
    sentry_url_prefix=None,
    sentry_release_name=None,
    run_setup=None,
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
        '-m': sentry_source_map_s3_url,
        '-p': sentry_url_prefix,
        '-r': sentry_release_name,
        '-s': run_setup
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
    runner.run('runSentryRelease.sh', [], options, env, _is_cli)
