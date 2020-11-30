import os
import re
import click

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.manage import stack as manage_stack_backend
from hamlet.backend import query as query_backend


def find_deployments_from_options(generation, deployment_mode, deployment_group, deployment_units):
    query_args = {
        'deployment_mode': deployment_mode,
        'generation_provider': generation.generation_provider,
        'generation_framework': generation.generation_framework,
        'generation_input_source': generation.generation_input_source,
        'generation_entrance': 'unitlist',
        'output_filename': 'unitlist-managementcontract.json',
        'refresh_output': True
    }
    available_deployments = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=LIST_DEPLOYMENTS_QUERY
    )

    deployments = []

    for deployment in available_deployments:
        if re.search(deployment_group, deployment['DeploymentGroup']):
            for unit_pattern in deployment_units:
                if re.search(unit_pattern, deployment['DeploymentUnit']):
                    deployments.append(deployment)

    return deployments


class Generation(object):
    def __init__(self, generation_provider=None, generation_framework=None, generation_input_source=None):
        self.generation_provider = generation_provider
        self.generation_framework = generation_framework
        self.generation_input_source = generation_input_source


pass_generation = click.make_pass_decorator(Generation, ensure=True)


@cli.group('deploy')
@click.pass_context
@click.option(
    '-p',
    '--generation-provider',
    help='provider for output generation',
    multiple=True,
    show_default=True
)
@click.option(
    '-f',
    '--generation-framework',
    help='output framework to use for output generation',
    default='cf',
    show_default=True
)
@click.option(
    '-i',
    '--generation-input-source',
    help='source of input data to use when generating the output',
    default='composite',
    show_default=True
)
def group(ctx, generation_provider, generation_framework, generation_input_source):
    """
    Deploys infrastructure based on the hamlet cmdb
    """
    ctx.obj = Generation(
        generation_provider=generation_provider,
        generation_framework=generation_framework,
        generation_input_source=generation_input_source
    )


LIST_DEPLOYMENTS_QUERY = (
    'Stages[].Steps[]'
    '.{'
    'DeploymentGroup:Parameters.DeploymentGroup,'
    'DeploymentUnit:Parameters.DeploymentUnit,'
    'DeploymentProvider:Parameters.DeploymentProvider,'
    'Operations:Parameters.Operations'
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
            ]
        )
    return tabulate(
        tablerows,
        headers=['DeploymentGroup', 'DeploymentUnit', 'DeploymentProvider'],
        tablefmt='github'
    )


@group.command(
    'list-deployments',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_generation
@click.option(
    '-m',
    '--deployment-mode',
    default='update',
    help='The deployment mode to use for the deployment'
)
@json_or_table_option(deployments_table)
def list_deployments(generation, deployment_mode):
    """
    List available deployments
    """
    args = {
        'deployment_mode': deployment_mode,
        'generation_provider': generation.generation_provider,
        'generation_framework': generation.generation_framework,
        'generation_input_source': generation.generation_input_source,
        'generation_entrance': 'unitlist',
        'output_filename': 'unitlist-managementcontract.json',
        'refresh_output': True
    }

    return query_backend.run(
        **args,
        cwd=os.getcwd(),
        query_text=LIST_DEPLOYMENTS_QUERY
    )


@group.command(
    'run-deployments',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_generation
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
def run_deployments(
        generation,
        deployment_mode,
        deployment_group,
        deployment_unit,
        output_dir,
        create,
        confirm,
        **kwargs):
    """
    Create and run deployments
    """

    deployments = find_deployments_from_options(generation, deployment_mode, deployment_group, deployment_unit)

    if len(deployments) == 0:
        click.echo(click.style('No deployments found that match pattern', bold=True, fg='red'))
        return -1

    for deployment in deployments:

        deployment_group = deployment['DeploymentGroup']
        deployment_unit = deployment['DeploymentUnit']
        click.echo('')
        click.echo((click.style(f'[*] {deployment_group}/{deployment_unit}', bold=True, fg='green')))
        click.echo('')

        if create:
            generate_args = {
                'generation_provider': generation.generation_provider,
                'generation_framework': generation.generation_framework,
                'generation_input_source': generation.generation_input_source,
                'entrance': 'deployment',
                'deployment_group': deployment_group,
                'deployment_unit': deployment_unit,
                'output_dir': output_dir
            }
            create_template_backend.run(**generate_args, _is_cli=True)

        for operation in deployment['Operations']:

            if (confirm and click.confirm(f'Start Deployment of ${deployment_group}/${deployment_unit} ?')) or not confirm:

                if deployment['DeploymentProvider'] == 'aws':
                    manage_args = {
                        'level': deployment_group,
                        'deployment_unit': deployment_unit,
                        'output_dir': output_dir
                    }

                    if operation == 'delete':
                        manage_args['delete'] = True

                    manage_stack_backend.run(**manage_args, _is_cli=True)


@group.command(
    'create-deployments',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_generation
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
def create_deployments(generation, deployment_mode, deployment_group, deployment_unit, output_dir, **kwargs):
    """
    Create deployment outputs
    """

    deployments = find_deployments_from_options(generation, deployment_mode, deployment_group, deployment_unit)

    if len(deployments) == 0:
        click.echo(click.style('No deployments found that match pattern', bold=True, fg='red'))
        return -1

    for deployment in deployments:

        deployment_group = deployment['DeploymentGroup']
        deployment_unit = deployment['DeploymentUnit']
        click.echo(f'[*] {deployment_group}/{deployment_unit}')

        generate_args = {
            'generation_provider': generation.generation_provider,
            'generation_framework': generation.generation_framework,
            'generation_input_source': generation.generation_input_source,
            'entrance': 'deployment',
            'deployment_group': deployment_group,
            'deployment_unit': deployment_unit,
            'output_dir': output_dir
        }
        create_template_backend.run(**generate_args, _is_cli=False)


@group.command(
    'test-deployments',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_generation
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
def test_deployments(generation, deployment_mode, deployment_group, deployment_unit, output_dir, **kwargs):
    """
    Test deployment outputs
    """

    deployments = find_deployments_from_options(generation, deployment_mode, deployment_group, deployment_unit)

    if len(deployments) == 0:
        click.echo(click.style('No deployments found that match pattern', bold=True, fg='red'))
        return -1

    for deployment in deployments:

        deployment_group = deployment['DeploymentGroup']
        deployment_unit = deployment['DeploymentUnit']
        click.echo(f'[*] {deployment_group}/{deployment_unit}')

        generate_args = {
            'generation_provider': generation.generation_provider,
            'generation_framework': generation.generation_framework,
            'generation_input_source': generation.generation_input_source,
            'entrance': 'deploymenttest',
            'deployment_group': deployment_group,
            'deployment_unit': deployment_unit,
            'output_dir': output_dir
        }
        create_template_backend.run(**generate_args, _is_cli=False)
