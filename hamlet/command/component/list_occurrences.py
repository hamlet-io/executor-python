import click

from tabulate import tabulate

from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common.config import pass_options
from hamlet.command.common import exceptions

from .common import query_occurrences_state

LIST_OCCURRENCES_QUERY = (
    'Occurrences[]'
    '.{'
    'TierId:Core.Tier.Id,'
    'ComponentId:Core.Component.RawId,'
    'Name:Core.RawName,'
    'Type:Core.Type'
    '}'
)


def list_occurrences_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['TierId']),
                wrap_text(row['ComponentId']),
                wrap_text(row['Name']),
                wrap_text(row['Type']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['TierId', 'ComponentId', 'Name', 'Type'],
        tablefmt='github'
    )


@click.command(
    'list-occurrences',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-q',
    '--query',
    help='A JMESPath query to apply to the results',
)
@json_or_table_option(list_occurrences_table)
@exceptions.backend_handler()
@pass_options
def list_occurrences(options, query):
    """
    List available occurrences
    """
    return query_occurrences_state(
        options=options,
        query=LIST_OCCURRENCES_QUERY,
        sub_query_text=query
    )
