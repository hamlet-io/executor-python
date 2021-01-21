import os
import re
import click

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common.exceptions import CommandError
from hamlet.backend import query as query_backend
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.manage import stack as manage_stack_backend
from hamlet.backend.manage import deployment as manage_deployment_backend
from hamlet.backend.common.exceptions import BackendException

def find_schemas_from_options(generation, deployment_group, deployment_units):
    query_args = {
        'deployment_mode': '',
        'generation_entrance': 'schemaset',
        'generation_input_source': generation.generation_input_source,
        'generation_provider': generation.generation_provider,
        'generation_framework': generation.generation_framework,
        'output_filename': 'schemaset-' + deployment_group + '-schemacontract.json',
        'refresh_output': True
    }
    try:
        available_schemas = query_backend.run(
            **query_args,
            cwd=os.getcwd(),
            query_text=LIST_SCHEMAS_QUERY
        )

    except BackendException as e:
        raise CommandError(str(e))

    deployments = []

    for schema in available_schemas:
        if re.fullmatch(deployment_group, schema['DeploymentGroup']):
            for deployment_unit in deployment_units:
                if re.fullmatch(deployment_unit, schema['DeploymentUnit']):
                    deployments.append(schema)

    return deployments

class Generation(object):
    def __init__(self, generation_provider=None, generation_framework=None, generation_input_source=None):
        self.generation_provider = generation_provider
        self.generation_framework = generation_framework
        self.generation_input_source = generation_input_source


pass_generation = click.make_pass_decorator(Generation, ensure=True)

@cli.group('schema')
@click.pass_context
@click.option(
    '-p',
    '--generation-provider',
    help='provider for output generation',
    default=['aws'],
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
    Generates JSONSchema files for Hamlet data types
    """
    ctx.obj = Generation(
        generation_provider=generation_provider,
        generation_framework=generation_framework,
        generation_input_source=generation_input_source
    )

LIST_SCHEMAS_QUERY = (
    'Stages[].Steps[]'
    '.{'
    'DeploymentGroup:Parameters.DeploymentGroup,'
    'DeploymentUnit:Parameters.DeploymentUnit,'
    'DeploymentProvider:Parameters.DeploymentProvider'
    '}'
)

def schema_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['DeploymentGroup']),
                wrap_text(row['DeploymentUnit']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['DeploymentGroup', 'DeploymentUnit'],
        tablefmt='github'
    )

@group.command(
    'list-schemas',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_generation
@click.option(
    '-l',
    '--deployment-group',
    required=True,
    show_default=True,
    help='The deployment group pattern to match',
)
@json_or_table_option(schema_table)
def list_schemas(generation, deployment_group):
    """
    List the available JSON schemas by data type
    """

    return find_schemas_from_options(generation, deployment_group, ['.*'])


@group.command(
    'create-schemas',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_generation
@click.option(
    '-l',
    '--deployment-group',
    required=True,
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
    required=True,
    help='the directory where the outputs will be saved'
)
def create_schemas(
    generation,
    deployment_group,
    deployment_unit,
    output_dir,
    **kwargs):
    """
    Create Hamlet data type schemas
    """

    schemas = find_schemas_from_options(generation, deployment_group, deployment_unit)

    if len(schemas) == 0:
        raise click.UsageError(click.style('No schemas found', bold=True, fg='red'))

    for schema in schemas:
        deployment_group = schema['DeploymentGroup']
        deployment_unit = schema['DeploymentUnit']
        click.echo('')
        click.echo((click.style(f'[*] Schema: {deployment_group}/{deployment_unit}', bold=True, fg='green')))
        click.echo('')

        schemaset_args = {
            'generation_provider': generation.generation_provider,
            'generation_framework': generation.generation_framework,
            'generation_input_source': generation.generation_input_source,
            'entrance': 'schemaset',
            'deployment_group': deployment_group,
            'output_dir': output_dir
        }

        try:
            create_template_backend.run(**schemaset_args, _is_cli=True)

        except BackendException as e:
            raise CommandError('SchemaSet Generation failed: ' + str(e))

        template_args = {
            'entrance': 'schema',
            'deployment_group': deployment_group,
            'deployment_unit': deployment_unit,
            'generation_provider': generation.generation_provider,
            'generation_framework': generation.generation_framework,
            'generation_input_source': generation.generation_input_source,
            'output_dir': output_dir
        }

        try:
            create_template_backend.run(**template_args, _is_cli=True)

        except BackendException as e:
            raise CommandError('Schema Generation failed')

