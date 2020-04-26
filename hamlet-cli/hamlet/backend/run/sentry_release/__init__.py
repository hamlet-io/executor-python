from hamlet.backend.common import runner


def run(
    sentry_source_map_s3_url=None,
    sentry_url_prefix=None,
    sentry_release_name=None,
    run_setup=None,
    _is_cli=False
):
    options = {
        '-m': sentry_source_map_s3_url,
        '-p': sentry_url_prefix,
        '-r': sentry_release_name,
        '-s': run_setup
    }
    runner.run('runSentryRelease.sh', [], options, _is_cli)
