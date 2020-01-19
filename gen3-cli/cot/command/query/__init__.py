import os
import json
import click
from cot.backend.common import exceptions
from cot.backend import query as query_backend
from cot.command import root


@root.command(
    'query',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-i',
    '--blueprint-generation-input-source',
    help='source of input data to use when generating the template'
)
@click.option(
    '-p',
    '--blueprint-generation-provider',
    help='provider to for template generation',
    default='aws',
    show_default=True
)
@click.option(
    '-f',
    '--blueprint-generation-framework',
    help='output framework to use for template generation',
    default='cf',
    show_default=True
)
@click.option(
    '-s',
    '--blueprint-generation-scenarios',
    help='comma seperated list of framework scenarios to load'
)
@click.option(
    '-q',
    '--query',
    help='JMESPath query'
)
@click.option(
    '-t',
    '--list-tiers',
    is_flag=True,
    help='print a table of blueprint tiers'
)
@click.option(
    '-c',
    '--list-components',
    is_flag=True,
    help='print a table of blueprint components'
)
@click.option(
    '-r',
    '--blueprint-refresh',
    is_flag=True,
    help='force refresh blueprint'
)
@exceptions.handler()
def query(**kwargs):
    result = query_backend.run(**kwargs, cwd=os.getcwd(), _is_cli=True)
    for key, value in result.items():
        if len(result) > 1:
            click.echo(key.upper())
        if key == 'query':
            value = json.dumps(value, indent=4)
        click.echo(value)
