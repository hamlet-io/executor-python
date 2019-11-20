import subprocess
from cot import utils
from cot import env


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
    version=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'runTask.sh',
        options={
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
    )

    subprocess.run(
        script_call_line,
        shell=True
    )
