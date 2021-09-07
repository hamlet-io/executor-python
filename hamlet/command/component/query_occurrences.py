import click
import json

from hamlet.command.common.config import pass_options
from hamlet.command.common import exceptions

from .common import query_occurrences_state


@click.command(
    "query-occurrences", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-q",
    "--query",
    required=True,
    help="A JMESPath query to apply to the results",
)
@exceptions.backend_handler()
@pass_options
def query_occurrences(options, query):
    """
    Run a query over all occurrences
    """
    result = query_occurrences_state(options=options, query=query)
    click.echo(json.dumps(result, indent=4))
