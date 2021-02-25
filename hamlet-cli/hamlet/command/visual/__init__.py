import os
import click
import re
import tempfile

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common.exceptions import CommandError
from hamlet.command.common.context import pass_generation, generation_config
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.draw import diagram as create_diagram_backend
from hamlet.backend import query as query_backend
from hamlet.backend.common.exceptions import BackendException


LIST_DIAGRAMS_QUERY = (
    'Diagrams[]'
    '.{'
    'Id:Id,'
    'Type:Type,'
    'Description:Description'
    '}'
)


def find_diagrams_from_options(generation, ids):
    query_args = {
        'generation_provider': generation.generation_provider,
        'generation_framework': generation.generation_framework,
        'generation_input_source': generation.generation_input_source,
        'generation_entrance': 'diagraminfo',
        'output_filename': 'diagraminfo.json',
        'use_cache': False
    }
    try:
        available_diagrams = query_backend.run(
            **query_args,
            cwd=os.getcwd(),
            query_text=LIST_DIAGRAMS_QUERY
        )

    except BackendException as e:
        raise CommandError(str(e))

    diagrams = []

    for diagram in available_diagrams:
        for id in ids:
            if re.fullmatch(id, diagram['Id']):
                diagrams.append(diagram)

    return diagrams


@cli.group('visual')
@generation_config
def group():
    """
    Generates visual representations of your hamlet
    """
    pass


def diagrams_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['Id']),
                wrap_text(row['Type']),
                wrap_text(row['Description']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['Id', 'Type', 'Description'],
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
@click.option(
    '-i',
    '--diagram-id',
    default=['.*'],
    show_default=True,
    multiple=True,
    help='The deployment id pattern to match'
)
@json_or_table_option(diagrams_table)
@pass_generation
def list_diagrams(generation, diagram_id):
    """
    Lists the diagrams available to create
    """
    return find_diagrams_from_options(generation, diagram_id)


@group.command(
    'draw-diagrams',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-s',
    '--src-dir',
    required=False,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    default=None,
    help='the directory to save the generation scripts to - temp dir by default'
)
@click.option(
    '-d',
    '--asset-dir',
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    help='the directory to save the generated diagrams to'
)
@click.option(
    '-i',
    '--diagram-id',
    default=['.*'],
    show_default=True,
    multiple=True,
    help='The diagram id pattern to match'
)
@pass_generation
def draw_diagrams(generation, diagram_id, src_dir, asset_dir):
    """
    Draw a collection of digrams based on your solution
    """
    temp_dir = None

    if src_dir is None:
        temp_dir = tempfile.TemporaryDirectory()
        src_dir = temp_dir.name

    diagrams = find_diagrams_from_options(generation, diagram_id)

    if len(diagrams) == 0:
        raise CommandError('No diagrams found that match pattern')

    for diagram in diagrams:

        diagram_id = diagram['Id']

        click.echo((click.style(f'[*] {diagram_id}', bold=True, fg='green')))
        args = {
            "generation_provider": generation.generation_provider,
            "generation_framework": generation.generation_framework,
            "generation_input_source": generation.generation_input_source,
            "entrance": 'diagram',
            'deployment_unit': diagram_id,
            'output_dir': src_dir
        }
        try:
            create_template_backend.run(**args, _is_cli=False)
        except BackendException as e:
            raise CommandError(str(e))

        try:
            create_diagram_backend.run(diagram_id=diagram_id, src_dir=src_dir, output_dir=asset_dir)
        except BackendException as e:
            raise CommandError(str(e))

    if temp_dir is not None:
        temp_dir.cleanup()


LIST_DIAGRAM_TYPES_QUERY = (
    'DiagramTypes[]'
    '.{'
    'Type:Type,'
    'Description:Description'
    '}'
)


def diagram_types_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['Type']),
                wrap_text(row['Description']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['Type', 'Description'],
        showindex=True,
        tablefmt="fancy_grid"
    )


@group.command(
    'list-diagram-types',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@json_or_table_option(diagram_types_table)
@pass_generation
def list_diagram_types(generation):
    """
    Lists the types of diagrams available
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
        query_text=LIST_DIAGRAM_TYPES_QUERY
    )
