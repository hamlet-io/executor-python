import subprocess
from cot import utils
from cot import env


def run(
    function_id=None,
    deployment_unit=None,
    input_payload=None,
    include_log_tail=None
):
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'runLambda.sh',
        options={
            '-f': function_id,
            '-u': deployment_unit,
            '-i': input_payload,
            '-l': include_log_tail
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
