import os
import click
import json

from tabulate import tabulate

from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common import config, exceptions
from hamlet.backend import query as query_backend


def query_info_output(options, engine, query, query_params=None, sub_query_text=None):
    query_args = {
        **options.opts,
        "generation_entrance": "info",
        "output_filename": "info.json",
    }
    query_result = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=query,
        query_params=query_params,
        sub_query_text=sub_query_text,
        engine=engine
    )

    return query_result


def component_types_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Type"]),
                wrap_text(row["Description"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=["Type", "Description"],
        tablefmt="github",
    )


@click.command(
    "list-component-types", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="A query to filter out the results")
@json_or_table_option(component_types_table)
@exceptions.backend_handler()
@config.pass_options
def list_component_types(options, query):
    """
    Lists the types of components available
    """

    LIST_COMPONENT_TYPES_QUERY = (
        "ComponentTypes[]" ".{" "Type:Type," "Description:Description" "}"
    )

    return query_info_output(
        options, options.engine, LIST_COMPONENT_TYPES_QUERY, None, query
    )


@click.command(
    "describe-component-type",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "-t", "--type", required=True, help="The type of the component to describe"
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@config.pass_options
def describe_component_type(options, type, query):
    """
    Describes a specific component type
    """
    DESCRIBE_COMPONENT_TYPE_QUERY = "ComponentTypes[?Type=={type}] | [0]"

    click.echo(
        json.dumps(
            query_info_output(
                options,
                options.engine,
                DESCRIBE_COMPONENT_TYPE_QUERY,
                {"type": type},
                query,
            ),
            indent=2,
        )
    )


@click.command(
    "query-component-types", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@config.pass_options
def query_component_types(options, query):
    """
    Query across all component types
    """
    click.echo(
        json.dumps(
            query_info_output(options, options.engine, "ComponentTypes[]", None, query),
            indent=2,
        )
    )
