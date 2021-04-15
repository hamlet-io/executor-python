import click

from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.manage import stack as manage_stack_backend
from hamlet.backend.manage import deployment as manage_deployment_backend

from .util import find_deployments_from_options

@click.command(
    'run-deployments',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-m',
    '--deployment-mode',
    default='update',
    help='The deployment mode to use for the deployment'
)
@click.option(
    '-l',
    '--deployment-group',
    default='.*',
    show_default=True,
    help='The deployment group pattern to match',
)
@click.option(
    '-u',
    '--deployment-unit',
    default=['.*'],
    show_default=True,
    multiple=True,
    help='The deployment unit pattern to match'
)
@click.option(
    '-s',
    '--deployment-state',
    type=click.Choice(
        ['deployed', 'notdeployed', 'orphaned', ],
        case_sensitive=False,
    ),
    default=['deployed', 'notdeployed'],
    multiple=True,
    help='The states of deployments to include'
)
@click.option(
    '-o',
    '--output-dir',
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    help='the directory where the outputs will be saved'
)
@click.option(
    '--refresh-outputs/--no-refresh-outputs',
    default=True,
    help='Update outputs or use existing'
)
@click.option(
    '--confirm/--no-confirm',
    default=False,
    help='Confirm before executing each deployment'
)
@exceptions.backend_handler()
@pass_options
def run_deployments(
        options,
        deployment_mode,
        deployment_group,
        deployment_unit,
        deployment_state,
        output_dir,
        refresh_outputs,
        confirm,
        **kwargs):
    """
    Create and run deployments
    """
    deployments = find_deployments_from_options(
                    options=options,
                    deployment_mode=deployment_mode,
                    deployment_group=deployment_group,
                    deployment_units=deployment_unit,
                    deployment_states=deployment_state
                )

    if len(deployments) == 0:
        raise exceptions.CommandError('No deployments found that match pattern')

    for deployment in deployments:

        deployment_group = deployment['DeploymentGroup']
        deployment_unit = deployment['DeploymentUnit']
        deployment_state = deployment['CurrentState']

        click.echo('')
        click.echo((click.style(f'[*] {deployment_group}/{deployment_unit}', bold=True, fg='green')))

        if deployment_state == 'orphaned':
            click.echo((click.style(f'[-] deployment has been orphaned, running orphan clean up', bold=False, fg='yellow')))

        click.echo('')

        if refresh_outputs:
            if deployment_state != 'orphaned':
                generate_args = {
                    **options.opts,
                    'entrance': 'deployment',
                    'deployment_group': deployment_group,
                    'deployment_unit': deployment_unit,
                    'output_dir': output_dir
                }
                create_template_backend.run(**generate_args, _is_cli=True)

        for operation in deployment['Operations']:

            if (
                (confirm and click.confirm(f'Start Deployment of {deployment_group}/{deployment_unit} ?'))
                or not confirm
            ):

                manage_args = {
                    **options.opts,
                    'deployment_group': deployment_group,
                    'deployment_unit': deployment_unit,
                    'output_dir': output_dir
                }

                if operation == 'delete':
                    manage_args['delete'] = True

                supported_deployment_provider = False
                if deployment['DeploymentProvider'] == 'aws':
                    supported_deployment_provider = True
                    manage_stack_backend.run(**manage_args, _is_cli=True)

                if deployment['DeploymentProvider'] == 'azure':
                    supported_deployment_provider = True
                    manage_deployment_backend.run(**manage_args, _is_cli=True)

                if not supported_deployment_provider:
                    deployment_provider = deployment.get('DeploymentProvider', None)
                    raise exceptions.CommandError(f'Deployment provider {deployment_provider} is not supported')
