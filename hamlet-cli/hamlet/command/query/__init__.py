import os
import json
import click
from tabulate import tabulate
from hamlet.backend.common import exceptions
from hamlet.backend import query as query_backend
from hamlet.command import root
from hamlet.command.common.display import json_or_table_option, wrap_text


def tiers_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['Id']),
                wrap_text(row['Name']),
                wrap_text(row['Description']),
                row['NetworkEnabledState']
            ]
        )
    return tabulate(
        tablerows,
        headers=['Id', 'Name', 'Description', 'NetworkEnabledState'],
        showindex=True,
        tablefmt="fancy_grid"
    )


def components_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['Id']),
                wrap_text(row['Type']),
                wrap_text(row['Name']),
                wrap_text(row['TierId'])
            ]
        )
    return tabulate(
        tablerows,
        headers=['Id', 'Type', 'Name', 'TierId'],
        showindex=True,
        tablefmt="fancy_grid"
    )


def key_value_table(data):
    tablerows = []
    for item in data:
        tablerows.append([wrap_text(item['Key']), wrap_text(item['Value'])])
    return tabulate(
        tablerows,
        headers=['Key', 'Value'],
        showindex=True,
        tablefmt="fancy_grid"
    )


def occurrences_table(data):
    tablerows = []
    for item in data:
        tablerows.append(
            [
                wrap_text(item['InstanceId']),
                wrap_text(item['VersionId']),
                wrap_text(item['FullName']),
                wrap_text(', '.join(item.get('DeploymentUnits', []))),
                item['Enabled']
            ]
        )
    return tabulate(
        tablerows,
        headers=['InstanceId', 'VersionId', 'FullName', 'DeploymentUnits', 'Enabled'],
        showindex=True,
        tablefmt="fancy_grid"
    )


@root.group(
    'query',
    context_settings=dict(
        max_content_width=240
    )
)
@click.pass_context
@click.option(
    '-i',
    '--generation-input-source',
    help='source of input data to use when generating the template'
)
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
    help='output framework to use for template generation',
    default='cf',
    show_default=True
)
@click.option(
    '-r',
    '--refresh-output',
    is_flag=True,
    help='force refresh blueprint'
)
def query_group(ctx, **kwargs):
    """
    Base command used to set blueprint generation options
    """
    blueprint_args = {
        "generation_entrance": 'blueprint',
        'output_filename': 'blueprint-config.json',
        **kwargs
    }
    ctx.obj = dict(blueprint=blueprint_args)


@query_group.command('get')
@click.argument('query_text')
@click.pass_context
@exceptions.handler()
def get(ctx, query_text):
    """
    JMESPath query
    """
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_text=query_text
    )
    click.echo(json.dumps(result, indent=4))


@query_group.group('describe')
@click.pass_context
def describe_group(ctx):
    """
    Queries category
    """


@describe_group.group('occurrence', invoke_without_command=True)
@click.pass_context
@click.option(
    '-t',
    '--tier-id',
    'tier_id',
    required=True
)
@click.option(
    '-c',
    '--component-id',
    'component_id',
    required=True
)
@click.option(
    '-i',
    '--instance-id',
    'instance_id',
    default=''
)
@click.option(
    '-v',
    '--version-id',
    'version_id',
    default=''
)
@exceptions.handler()
def describe_occurrence(ctx, **query_params):
    """
    Describes occurrence
    """
    if ctx.invoked_subcommand is not None:
        ctx.obj['query_params'] = query_params
        return
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='describe_occurrence',
        query_params=query_params
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('get')
@click.argument('query_text')
@click.pass_context
@exceptions.handler()
def describe_occurrence_get(ctx, query_text):
    """
    JMESPath subquery on the described occurrence data
    """
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='describe_occurrence',
        query_params=ctx.obj['query_params'],
        sub_query_text=query_text
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('attributes')
@click.pass_context
@exceptions.handler()
@json_or_table_option(key_value_table)
def describe_occurrence_attributes(ctx):
    """
    Describes occurrence attributes
    """
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='describe_occurrence_attributes',
        query_params=ctx.obj['query_params']
    )
    return result


@describe_occurrence.command('solution')
@click.pass_context
@exceptions.handler()
def describe_occurrence_solution(ctx):
    """
    Describes occurrence solution
    """
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='describe_occurrence_solution',
        query_params=ctx.obj['query_params']
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('settings')
@click.pass_context
@exceptions.handler()
def describe_occurrence_settings(ctx):
    """
    Describes occurrence settings
    """
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='describe_occurrence_settings',
        query_params=ctx.obj['query_params']
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('resources')
@click.pass_context
@exceptions.handler()
def describe_occurrence_resources(ctx):
    """
    Describes occurrence resources
    """
    result = query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='describe_occurrence_resources',
        query_params=ctx.obj['query_params']
    )
    click.echo(json.dumps(result, indent=4))


@query_group.group('list')
@click.pass_context
def list_group(ctx):
    """
    Queries category
    """


@list_group.command('tiers')
@click.pass_context
@exceptions.handler()
@json_or_table_option(tiers_table)
def list_tiers(ctx):
    """
    List tiers
    """
    return query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='list_tiers'
    )


@list_group.command('components')
@click.pass_context
@exceptions.handler()
@json_or_table_option(components_table)
def list_components(ctx):
    """
    List components
    """
    return query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='list_components'
    )


@list_group.command('occurrences')
@click.pass_context
@click.option(
    '-t',
    '--tier-id',
    'tier_id',
    required=True
)
@click.option(
    '-c',
    '--component-id',
    'component_id',
    required=True
)
@exceptions.handler()
@json_or_table_option(occurrences_table)
def list_occurrences(ctx, **query_params):
    """
    List occurrences
    """
    return query_backend.run(
        **ctx.obj['blueprint'],
        cwd=os.getcwd(),
        query_name='list_occurrences',
        query_params=query_params
    )
