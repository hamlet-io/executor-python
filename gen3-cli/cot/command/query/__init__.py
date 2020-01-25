import os
import json
import textwrap
import click
from tabulate import tabulate
from cot.backend.common import exceptions
from cot.backend import query as query_backend
from cot.command import root


MAX_TABLE_TEXT_CONTENT_WIDTH = 128


@root.group('query')
def query():
    pass


def blueprint_generation_options(func):
    options = []
    options.append(
        click.option(
            '-i',
            '--blueprint-generation-input-source',
            help='source of input data to use when generating the template'
        )
    )
    options.append(
        click.option(
            '-p',
            '--blueprint-generation-provider',
            help='provider to for template generation',
            default='aws',
            show_default=True
        )
    )
    options.append(
        click.option(
            '-f',
            '--blueprint-generation-framework',
            help='output framework to use for template generation',
            default='cf',
            show_default=True
        )
    )
    options.append(
        click.option(
            '-s',
            '--blueprint-generation-scenarios',
            help='comma seperated list of framework scenarios to load'
        )
    )
    options.append(
        click.option(
            '-r',
            '--blueprint-refresh',
            is_flag=True,
            help='force refresh blueprint'
        )
    )
    for decorator in options[::-1]:
        func = decorator(func)
    return func


@query.command('get')
@click.option(
    '-q',
    '--query',
    help='JMESPath query',
    required=True
)
@blueprint_generation_options
@exceptions.handler()
def get(**kwargs):
    result = query_backend.run(**kwargs, cwd=os.getcwd(), _is_cli=True)
    click.echo(json.dumps(result.get('query'), indent=4))


@query.command('list-tiers')
@blueprint_generation_options
@exceptions.handler()
def list_tiers(**kwargs):
    result = query_backend.run(**kwargs, list_tiers=True, cwd=os.getcwd(), _is_cli=True)
    click.echo(tiers_table(result['tiers']))


@query.command('list-components')
@blueprint_generation_options
@exceptions.handler()
def list_components(**kwargs):
    result = query_backend.run(**kwargs, list_components=True, cwd=os.getcwd(), _is_cli=True)
    click.echo(components_table(result['components']))


def wrap_text(text):
    if text is None:
        return "None"
    return "\n".join(textwrap.wrap(text, MAX_TABLE_TEXT_CONTENT_WIDTH))


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
                wrap_text(row['Name'])
            ]
        )
    return tabulate(
        tablerows,
        headers=['Id', 'Type', 'Name'],
        showindex=True,
        tablefmt="fancy_grid"
    )
