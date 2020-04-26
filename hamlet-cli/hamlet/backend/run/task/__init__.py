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
    _is_cli=False
):
    options = {
        '-c': container_id,
        '-d': delay,
        '-e': env_name,
        '-i': component,
        '-j': component_instance,
        '-k': component_version,
        '-t': tier,
        '-v': value,
        '-w': task,
        '-x': instance,
        '-y': version
    }
    runner.run('runTask.sh', [], options, _is_cli)
