from cot.backend.common import runner


def run(
    component=None,
    tier=None,
    instance=None,
    version=None,
    pipeline_status_only=None,
    pipeline_allow_concurrent=None,
    _is_cli=False
):
    options = {
        '-i': component,
        '-t': tier,
        '-x': instance,
        '-y': version,
        '-s': pipeline_status_only,
        '-c': pipeline_allow_concurrent
    }
    runner.run('runPipeline.sh', [], options, _is_cli)
