import click
from hamlet.backend.run import lambda_func as run_lambda_func_backend
from hamlet.backend.common.exceptions import BackendException
from hamlet.command.common.exceptions import CommandError

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
    try:
        run_lambda_func_backend.run(**kwargs, _is_cli=True)
    except BackendException as e:
        raise CommandError(str(e))
