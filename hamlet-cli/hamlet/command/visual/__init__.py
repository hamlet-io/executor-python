import os
import click


from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common.exceptions import CommandError
from hamlet.command.common.context import pass_generation, generation_config
from hamlet.backend.create import template as create_template_backend
from hamlet.backend import query as query_backend
from hamlet.backend.common.exceptions import BackendException


class Generation(object):
    def __init__(self, generation_provider=None, generation_framework=None, generation_input_source=None):
        self.generation_provider = generation_provider
        self.generation_framework = generation_framework
        self.generation_input_source = generation_input_source


pass_generation = click.make_pass_decorator(Generation, ensure=True)


@cli.group('visual')
@generation_config
def group():
    """
    Generates visual representations of your hamlet deployment
    """
    pass


LIST_DIAGRAMS_QUERY = (
    'Diagrams[]'
    '.{'
    'Name:Name,'
    'Type:Type,'
    'DeploymentGroup:DeploymentGroup,'
    'Description:Description'
    '}'
)


def diagrams_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['Name']),
                wrap_text(row['Type']),
                wrap_text(row['DeploymentGroup']),
                wrap_text(row['Description']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['Name', 'Type', 'DeploymentGroup', 'Description'],
        showindex=True,
        tablefmt="fancy_grid"
    )


@group.command(
    'list-diagrams',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@json_or_table_option(diagrams_table)
@pass_generation
def list_diagrams(generation):
    """
    List available diagrams
    """
    args = {
        'generation_provider': generation.generation_provider,
        'generation_framework': generation.generation_framework,
        'generation_input_source': 'mock',
        'generation_entrance': 'diagraminfo',
        'output_filename': 'diagraminfo.json',
        'use_cache': False
    }

    return query_backend.run(
        **args,
        cwd=os.getcwd(),
        query_text=LIST_DIAGRAMS_QUERY
    )


@group.command(
    'draw-diagram',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-l',
    '--deployment-group',
    required=True,
    help='output level',
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
@pass_generation
@click.option(
    '-x',
    '--disable-output-cleanup',
    is_flag=True,
    help='disable the cleanup of the output directory before generation',
)
def draw_diagram(generation, **kwargs):
    """
    Invoke a Hamlet Entrance
    """
    args = {
        "generation_provider": generation.generation_provider,
        "generation_framework": generation.generation_framework,
        "generation_input_source": generation.generation_input_source,
        "entrance": 'diagram',
        **kwargs
    }
    try:
        create_template_backend.run(**args, _is_cli=True)
    except BackendException as e:
        raise CommandError(str(e))
