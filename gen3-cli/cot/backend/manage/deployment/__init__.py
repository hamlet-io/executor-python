import subprocess
from cot import utils
from cot import env


def run(
    delete=None,
    deployment_initiate=None,
    level=None,
    deployment_monitor=None,
    deployment_name=None,
    region=None,
    deployment_scope=None,
    deployment_unit=None,
    deployment_wait=None,
    deployment_unit_subset=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'manageDeployment.sh',
        options={
            '-d': delete,
            '-i': deployment_initiate,
            '-m': deployment_monitor,
            '-l': level,
            '-n': deployment_name,
            '-r': region,
            '-s': deployment_scope,
            '-u': deployment_unit,
            '-w': deployment_wait,
            '-z': deployment_unit_subset
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
