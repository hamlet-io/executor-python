import click
from cot.backend.run import pipeline as run_pipeline_backend


@click.command(
    'pipeline',
    short_help='Run an AWS Data pipeline',
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
def pipeline(**kwargs):
    """
    Run an AWS Data pipeline

    \b
    NOTES:
    1. This will activate the pipeline and leave it running
    2. Pipelines take a long time so it is better to provide status via other means
    """
    run_pipeline_backend.run(**kwargs, _is_cli=True)
