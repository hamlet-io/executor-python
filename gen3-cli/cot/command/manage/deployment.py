import subprocess
import click
from cot import env
from cot import utils


@click.command(context_settings=dict(max_content_width=240))
@click.option(
    '-d',
    '--delete',
    help='delete the deployment',
    is_flag=True
)
@click.option(
    '-i',
    '--deployment-initiate',
    help='initiate but do not monitor the deployment operation(disable monitoring)',
    is_flag=True
)
@click.option(
    '-l',
    '--level',
    type=click.Choice(
        [
            'account',
            'product',
            'segment',
            'solution',
            'application',
            'multiple'
        ],
        case_sensitive=False
    ),
    help='stack level',
    required=True
)
@click.option(
    '-m',
    '--deployment-monitor',
    help='monitor but do not initiate the deployment operation(disable initiation)',
    is_flag=True
)
@click.option(
    '-n',
    '--deployment-name',
    help='override the standard deployment naming'
)
@click.option(
    '-r',
    '--region',
    help='Azure location/region code for this deployment'
)
@click.option(
    '-s',
    '--deployment-scope',
    type=click.Choice(
        [
            'subscription',
            'resourceGroup'
        ],
        case_sensitive=False
    ),
    help='deployment scope',
    default='resourceGroup',
    show_default=True
)
@click.option(
    '-u',
    '--deployment-unit',
    required=True,
    help='deployment unit used to determine the deployment template'
)
@click.option(
    '-w',
    '--deployment-wait',
    type=click.INT,
    help='interval between checking the progress of a deployment operation',
    default=30,
    show_default=True
)
@click.option(
    '-z',
    '--deployment-unit-subset',
    help='subset of the deployment unit required'
)
def deployment(
    delete,
    deployment_initiate,
    level,
    deployment_monitor,
    deployment_name,
    region,
    deployment_scope,
    deployment_unit,
    deployment_wait,
    deployment_unit_subset
):
    """
    Manage an Azure Resource Manager (ARM) deployment
    """
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'manageDeployment.sh',
        options={
            '-d': delete,
            '-i': deployment_initiate,
            '-m': deployment_monitor,
            '-l': level,
            '-n': deployment_name,
            '-r': region,
            '-s': deployment_scope,
            '-u': deployment_unit,
            '-w': deployment_wait,
            '-z': deployment_unit_subset
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
