import subprocess
from cot import utils
from cot import env


def run(
    delete=None,
    stack_initiate=None,
    stack_monitor=None,
    stack_wait=None,
    stack_name=None,
    level=None,
    region=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    dryrun=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'manageStack.sh',
        options={
            '-d': delete,
            '-i': stack_initiate,
            '-m': stack_monitor,
            '-w': stack_wait,
            '-n': stack_name,
            '-r': region,
            '-y': dryrun,
            '-u': deployment_unit,
            '-z': deployment_unit_subset,
            '-l': level
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
