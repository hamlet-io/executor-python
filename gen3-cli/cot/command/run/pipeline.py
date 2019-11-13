import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'pipeline',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-i',
    '--component',
    help='name of the component in the solution where the task is defined',
    required=True
)
@click.option(
    '-t',
    '--tier',
    help='name of the tier in the solution where the task is defined',
    required=True
)
@click.option(
    '-x',
    '--instance',
    help='instance of the task to be run'
)
@click.option(
    '-y',
    '--version',
    help='version of the task to be run'
)
@click.option(
    '-s',
    '--pipeline-status-only',
    help='check the running status of a pipelie',
    is_flag=True
)
@click.option(
    '-c',
    '--pipeline-allow-concurrent',
    help='activate the pipeline if another one is running',
    is_flag=True
)
def pipeline(
    component,
    tier,
    instance,
    version,
    pipeline_status_only,
    pipeline_allow_concurrent
):
    """
    Run an AWS Data pipeline

    \b
    NOTES:
    1. This will activate the pipeline and leave it running
    2. Pipelines take a long time so it is better to provide status via other means
    """
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
