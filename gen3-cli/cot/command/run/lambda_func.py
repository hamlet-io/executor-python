import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'lambda',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-f',
    '--function-id',
    help='id of the function in the lambda deployment to run',
    required=True
)
@click.option(
    '-u',
    '--deployment-unit',
    help='lambda deployment unit you want to execute',
    required=True
)
@click.option(
    '-i',
    '--input-payload',
    help='json based payload you want to run the lambda with'
)
@click.option(
    '-l',
    '--include-log-tail',
    help='include the last 4kb of the execution log',
    is_flag=True
)
def lambda_func(
    function_id,
    deployment_unit,
    input_payload,
    include_log_tail
):
    """
    Run an AWS Lambda Function
    """
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
