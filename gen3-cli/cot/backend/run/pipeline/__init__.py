import subprocess
from cot import utils
from cot import env


def run(
    component=None,
    tier=None,
    instance=None,
    version=None,
    pipeline_status_only=None,
    pipeline_allow_concurrent=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'runPipeline.sh',
        options={
            '-i': component,
            '-t': tier,
            '-x': instance,
            '-y': version,
            '-s': pipeline_status_only,
            '-c': pipeline_allow_concurrent
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
