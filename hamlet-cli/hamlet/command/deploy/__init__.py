import os
import re
import click

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.manage import stack as manage_stack_backend
from hamlet.backend import query as query_backend


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
    'DeploymentProvider:Parameters.DeploymentProvider'
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
@json_or_table_option(deployments_table)
def list_deployments(generation):
    """
    List available deployments
    """
    args = {
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
    '-g',
    '--deployment-group',
    required=True,
    help='The deployment group pattern to match',
)
@click.option(
    '-u',
    '--deployment-unit',
    required=True,
    multiple=True,
    help='The deployment unit pattern to match'
)
@click.option(
    '-r',
    '--regex-match',
    is_flag=True,
    help='Treat group and units as regex patterns'
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
def run_deployments(generation, deployment_mode, deployment_group, deployment_unit, regex_match, output_dir, **kwargs):
    """
    Generate and run deployments
    """

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

    deployments=[]

    for deployment in available_deployments:
        if regex_match:
            if re.search(deployment_group, deployment['DeploymentGroup']):
                for unit_pattern in deployment_unit:
                    if re.search(unit_pattern, deployment['DeploymentUnit']):
                        deployments.append(deployment)
        else:
            if deployment_group == deployment['DeploymentGroup'] and deployment['DeploymentUnit'] in deployment_unit:
                deployments.append(deployment)

    if len(deployments) == 0:
        click.echo(click.style('No deployments found that match pattern', bold=True, fg='red'))
        return -1

    click.echo(click.style('Deployments Found:', bold=True))
    for deployment in deployments:
        deployment_group = deployment['DeploymentGroup']
        deployment_unit = deployment['DeploymentUnit']
        click.echo(f'[*] {deployment_group}/{deployment_unit}')

    click.echo()

    def show_deployment(deployment):
        if deployment is not None:
            deployment_group = deployment['DeploymentGroup']
            deployment_unit = deployment['DeploymentUnit']
            return f"{deployment_group}/{deployment_unit}"

    with click.progressbar(deployments, label='Running Deployments', item_show_func=show_deployment) as deployments_list:
        for deployment in deployments_list:
            generate_args = {
                'generation_provider': generation.generation_provider,
                'generation_framework': generation.generation_framework,
                'generation_input_source': generation.generation_input_source,
                'entrance' : 'deployment',
                'level' : deployment_group,
                'deployment_unit' : deployment_unit,
                'output_dir' : output_dir
            }
            create_template_backend.run(**generate_args, _is_cli=False)

            manage_args = {
                'level' : deployment_group,
                'deployment_unit' : deployment_unit,
                'output_dir' : output_dir
            }
            manage_stack_backend.run(**manage_args, _is_cli=False)
