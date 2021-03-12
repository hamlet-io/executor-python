import os
import json
import click
from tabulate import tabulate

from hamlet.command.common.config import pass_options, Options
from hamlet.command.common import exceptions
from hamlet.backend import query as query_backend
from hamlet.command import root
from hamlet.command.common.display import json_or_table_option, wrap_text


class BlueprintContext():
    '''Query Blueprint context'''
    def __init__(
            self,
            use_cache=False,
            query_params=None):
        self.backend = {
            'generation_entrance': 'blueprint',
            'output_filename': 'blueprint-config.json',
            'use_cache': use_cache,
        }
        self.query_params = query_params


pass_blueprint = click.make_pass_decorator(BlueprintContext, ensure=True)


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
@click.option(
    '-r',
    '--use-cache/--no-use-cache',
    default=False,
    is_flag=True,
    help='force refresh blueprint'
)
@click.pass_context
def query_group(ctx, use_cache):
    """
    Base command used to set blueprint generation options
    """
    ctx.obj = BlueprintContext(
        use_cache=use_cache
    )


@query_group.command('get')
@click.argument('query_text')
@exceptions.backend_handler()
@pass_options
@pass_blueprint
def get(blueprint_ctx, options, query_text):
    """
    JMESPath query
    """
    result = query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_text=query_text
    )
    click.echo(json.dumps(result, indent=4))


@query_group.group('describe')
@pass_blueprint
def describe_group(blueprint_ctx):
    """
    Queries category
    """


@describe_group.group('occurrence', invoke_without_command=True)
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
    default='default'
)
@click.option(
    '-v',
    '--version-id',
    'version_id',
    default='default'
)
@exceptions.backend_handler()
@click.pass_context
def describe_occurrence(ctx, **query_params):
    """
    Describes occurrence
    """
    if ctx.invoked_subcommand is not None:
        ctx.obj.query_params = query_params
        return

    blueprint_ctx = ctx.ensure_object(BlueprintContext)
    options = ctx.ensure_object(Options)

    result = query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='describe_occurrence',
        query_params=query_params
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('get')
@click.argument('query_text')
@exceptions.backend_handler()
@pass_options
@pass_blueprint
def describe_occurrence_get(blueprint_ctx, options, query_text):
    """
    JMESPath subquery on the described occurrence data
    """
    result = query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='describe_occurrence',
        query_params=blueprint_ctx.query_params,
        sub_query_text=query_text
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('attributes')
@exceptions.backend_handler()
@json_or_table_option(key_value_table)
@pass_options
@pass_blueprint
def describe_occurrence_attributes(blueprint_ctx, options):
    """
    Describes occurrence attributes
    """
    return query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='describe_occurrence_attributes',
        query_params=blueprint_ctx.query_params
    )


@describe_occurrence.command('solution')
@exceptions.backend_handler()
@pass_options
@pass_blueprint
def describe_occurrence_solution(blueprint_ctx, options):
    """
    Describes occurrence solution
    """
    result = query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='describe_occurrence_solution',
        query_params=blueprint_ctx.query_params
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('settings')
@exceptions.backend_handler()
@pass_options
@pass_blueprint
def describe_occurrence_settings(blueprint_ctx, options):
    """
    Describes occurrence settings
    """
    result = query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='describe_occurrence_settings',
        query_params=blueprint_ctx.query_params
    )
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command('resources')
@exceptions.backend_handler()
@pass_options
@pass_blueprint
def describe_occurrence_resources(blueprint_ctx, options):
    """
    Describes occurrence resources
    """
    result = query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='describe_occurrence_resources',
        query_params=blueprint_ctx.query_params
    )
    click.echo(json.dumps(result, indent=4))


@query_group.group('list')
@click.pass_context
def list_group(ctx):
    """
    Queries category
    """


@list_group.command('tiers')
@exceptions.backend_handler()
@json_or_table_option(tiers_table)
@pass_options
@pass_blueprint
def list_tiers(blueprint_ctx, options):
    """
    List tiers
    """
    return query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='list_tiers'
    )


@list_group.command('components')
@exceptions.backend_handler()
@json_or_table_option(components_table)
@pass_options
@pass_blueprint
def list_components(blueprint_ctx, options):
    """
    List components
    """
    return query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='list_components'
    )


@list_group.command('occurrences')
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
@exceptions.backend_handler()
@json_or_table_option(occurrences_table)
@pass_options
@pass_blueprint
def list_occurrences(blueprint_ctx, options, **query_params):
    """
    List occurrences
    """
    return query_backend.run(
        **blueprint_ctx.backend,
        **options.opts,
        cwd=os.getcwd(),
        query_name='list_occurrences',
        query_params=query_params
    )
