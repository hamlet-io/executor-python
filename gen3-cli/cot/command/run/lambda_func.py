import click
from cot.backend.run import lambda_func as run_lambda_func_backend


@click.command(
    'lambda',
    short_help='Run an AWS Lambda Function',
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
def lambda_func(**kwargs):
    """
    Run an AWS Lambda Function
    """
    run_lambda_func_backend.run(**kwargs)
