import os
import re
import click

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common.config import pass_options
from hamlet.backend import query as query_backend
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.manage import stack as manage_stack_backend
from hamlet.backend.manage import deployment as manage_deployment_backend


def find_deployments_from_options(options, deployment_mode, deployment_group, deployment_units, deployment_states):
    query_args = {
        **options.opts,
        'deployment_mode': deployment_mode,
        'generation_entrance': 'unitlist',
        'output_filename': 'unitlist-managementcontract.json',
        'use_cache': False,
    }
    available_deployments = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=LIST_DEPLOYMENTS_QUERY
    )

    deployments = []

    for deployment in available_deployments:
        if re.fullmatch(deployment_group, deployment['DeploymentGroup']):
            for deployment_unit in deployment_units:
                if re.fullmatch(deployment_unit, deployment['DeploymentUnit']):
                    if deployment['CurrentState'] in deployment_states:
                        deployments.append(deployment)

    return deployments


@cli.group('deploy')
def group():
    """
    Deploys infrastructure based on the hamlet cmdb
    """
    pass


LIST_DEPLOYMENTS_QUERY = (
    'Stages[].Steps[]'
    '.{'
    'DeploymentGroup:Parameters.DeploymentGroup,'
    'DeploymentUnit:Parameters.DeploymentUnit,'
    'DeploymentProvider:Parameters.DeploymentProvider,'
    'Operations:Parameters.Operations,'
    'CurrentState:Parameters.CurrentState'
    '}'
)


def deployments_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['DeploymentGroup']),
                wrap_text(row['DeploymentUnit']),
                wrap_text(row['DeploymentProvider']),
                wrap_text(row['CurrentState'])
            ]
        )
    return tabulate(
        tablerows,
        headers=['DeploymentGroup', 'DeploymentUnit', 'DeploymentProvider', 'CurrentState'],
        tablefmt='github'
    )


@group.command(
    'list-deployments',
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
@json_or_table_option(deployments_table)
@exceptions.backend_handler()
@pass_options
def list_deployments(options, deployment_mode, deployment_group, deployment_unit, deployment_state):
    """
    List available deployments
    """
    return find_deployments_from_options(
            options=options,
            deployment_mode=deployment_mode,
            deployment_group=deployment_group,
            deployment_units=deployment_unit,
            deployment_states=deployment_state
        )


@group.command(
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

        if refresh_outputs or deployment_state != 'orphaned' :
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


@group.command(
    'create-deployments',
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
        ['deployed', 'notdeployed',],
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
    help='the directory where the outputs will be saved. Mandatory when input source is set to mock'
)
@exceptions.backend_handler()
@pass_options
def create_deployments(options, deployment_mode, deployment_group, deployment_unit, deployment_state, output_dir, **kwargs):
    """
    Create deployment outputs
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
        click.echo(f'[*] {deployment_group}/{deployment_unit}')

        generate_args = {
            **options.opts,
            'entrance': 'deployment',
            'deployment_group': deployment_group,
            'deployment_unit': deployment_unit,
            'output_dir': output_dir
        }
        create_template_backend.run(**generate_args, _is_cli=True)
