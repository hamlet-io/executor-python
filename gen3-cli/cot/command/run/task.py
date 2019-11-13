import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'task',
    short_help='Run an ECS task',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-c',
    '--container-id',
    help='name of the container that environment details are applied to'
)
@click.option(
    '-d',
    '--delay',
    help='interval between checking the progress of the task',
    type=click.INT,
    default=30,
    show_default=True
)
@click.option(
    '-e',
    '--env',
    'env_name',
    help='name of an environment variable to define for the task'
)
@click.option(
    '-i',
    '--component',
    required=True,
    help='name of the ecs component in the solution where the task is defined'
)
@click.option(
    '-j',
    '--component-instance',
    help='instance of the ecs cluster to run the task on'
)
@click.option(
    '-k',
    '--component-version',
    help='version of the ecs clsuter to run the task on'
)
@click.option(
    '-t',
    '--tier',
    required=True,
    help='name of the tier in the solution where the task is defined'
)
@click.option(
    '-v',
    '--value',
    help='value for the last environment value defined (via -e) for the task'
)
@click.option(
    '-w',
    '--task',
    required=True,
    help='name of the task to be run',
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
def task(
    container_id,
    delay,
    env_name,
    component,
    component_instance,
    component_version,
    tier,
    value,
    task,
    instance,
    version
):
    """
    Run an ECS task

    \b
    NOTES:
    1. The ECS cluster is found using the provided tier and component combined with the product and segment
    2. ENV and VALUE should always appear in pairs
    """
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
