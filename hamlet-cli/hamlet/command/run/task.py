import click
from hamlet.backend.run import task as run_task_backend
from hamlet.backend.common.exceptions import BackendException
from hamlet.command.common.exceptions import CommandError

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
def task(**kwargs):
    """
    Run an ECS task

    \b
    NOTES:
    1. The ECS cluster is found using the provided tier and component combined with the product and segment
    2. ENV and VALUE should always appear in pairs
    """
    try:
        run_task_backend.run(**kwargs, _is_cli=True)
    except BackendException as e:
        raise CommandError(str(e))
