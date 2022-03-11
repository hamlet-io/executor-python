import os
import click
import json

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options
from hamlet.backend import query as query_backend


def query_info_output(options, query, query_params=None, sub_query_text=None):
    query_args = {
        **options.opts,
        "generation_entrance": "info",
        "output_filename": "info.json",
        "use_cache": False,
    }
    query_result = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=query,
        query_params=query_params,
        sub_query_text=sub_query_text,
        engine=options.engine
    )

    return query_result


@cli.group("reference", context_settings=dict(max_content_width=240))
def group():
    """
    Reference data provided in the CMDB
    """
    pass


def reference_types_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Type"]),
                wrap_text(row["PluralType"]),
                wrap_text(row["Description"]),
            ]
        )
    return tabulate(
        tablerows, headers=["Type", "PluralType", "Description"], tablefmt="github"
    )


@group.command(
    "list-reference-types", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="A query to filter out the reference results")
@json_or_table_option(reference_types_table)
@exceptions.backend_handler()
@pass_options
def list_reference_types(options, query):
    """
    Lists the types of references available
    """

    LIST_REFERENCE_TYPES_QUERY = (
        "ReferenceTypes[]"
        ".{"
        "Type:Type,"
        "PluralType:PluralType,"
        "Description:Description"
        "}"
    )

    return query_info_output(options, LIST_REFERENCE_TYPES_QUERY, None, query)


@group.command(
    "describe-reference-type",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "-t", "--type", required=True, help="The type of the reference to describe"
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def describe_reference_type(options, type, query):
    """
    Describes a specific reference type
    """
    DESCRIBE_REFERENCE_TYPE_QUERY = "ReferenceTypes[?Type=={type}] | [0]"

    click.echo(
        json.dumps(
            query_info_output(
                options, DESCRIBE_REFERENCE_TYPE_QUERY, {"type": type}, query
            ),
            indent=2,
        )
    )


@group.command(
    "query-reference-types", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def query_reference_types(options, query):
    """
    Query across all reference types
    """
    click.echo(
        json.dumps(
            query_info_output(options, "ReferenceTypes[]", None, query), indent=2
        )
    )


def reference_list_data_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Id"]),
                wrap_text(row["Type"]),
            ]
        )
    return tabulate(tablerows, headers=["Id", "Type"], tablefmt="github")


@group.command(
    "list-references", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="A query to filter out the reference results")
@json_or_table_option(reference_list_data_table)
@exceptions.backend_handler()
@pass_options
def list_references(options, query):
    """
    Lists the references available
    """

    LIST_REFERENCES_QUERY = "ReferenceData[].{Id:Id,Type:Type}"

    return query_info_output(options, LIST_REFERENCES_QUERY, {}, query)


@group.command(
    "describe-reference", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-t", "--type", required=True, help="The type of the reference to describe"
)
@click.option("-i", "--id", required=True, help="The id of the reference to describe")
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def describe_reference(options, type, id, query):
    """
    Describes a specific reference
    """
    DESCRIBE_REFERENCE_QUERY = "ReferenceData[?Type=={type} && Id=={id}] | [0]"

    click.echo(
        json.dumps(
            query_info_output(
                options, DESCRIBE_REFERENCE_QUERY, {"type": type, "id": id}, query
            ),
            indent=2,
        )
    )


@group.command(
    "query-references", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def query_references(options, query):
    """
    Query across all references
    """
    click.echo(
        json.dumps(query_info_output(options, "ReferenceData[]", None, query), indent=2)
    )
