import click
from cot.backend.manage import deployment as manage_deployment_backend


@click.command(
    'deployment',
    short_help='Manage an Azure Resource Manager (ARM) deployment',
    context_settings=dict(
        max_content_width=240
    )
)
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
def deployment(**kwargs):
    """
    Manage an Azure Resource Manager (ARM) deployment
    """
    manage_deployment_backend.run(**kwargs)
