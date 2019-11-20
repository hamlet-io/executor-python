import subprocess
from cot import utils
from cot import env


def run(
    config_ref=None,
    resource_group=None,
    level=None,
    request_ref=None,
    region=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    deployment_mode=None,
    generation_provider=None,
    generation_framework=None,
    generation_testcase=None,
    generation_scenarios=None,
    generation_input_source=None,
):
    options = {
        '-c': config_ref,
        '-g': resource_group,
        '-l': level,
        '-q': request_ref,
        '-r': region,
        '-u': deployment_unit,
        '-z': deployment_unit_subset,
        '-d': deployment_mode,
        '-p': generation_provider,
        '-f': generation_framework,
        '-t': generation_testcase,
        '-s': generation_scenarios,
        '-i': generation_input_source
    }
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'createTemplate.sh',
        args=[],
        options=options
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
