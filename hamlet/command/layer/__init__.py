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


@cli.group("layer", context_settings=dict(max_content_width=240))
def group():
    """
    Layers provided in the CMDB
    """
    pass


def layer_types_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Type"]),
                wrap_text(row["ReferenceLookupType"]),
                wrap_text(row["Description"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=["Type", "ReferenceLookupType", "Description"],
        tablefmt="github",
    )


@group.command(
    "list-layer-types", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="A query to filter out the results")
@json_or_table_option(layer_types_table)
@exceptions.backend_handler()
@pass_options
def list_layer_types(options, query):
    """
    Lists the types of layers available
    """

    LIST_LAYER_TYPES_QUERY = (
        "LayerTypes[]"
        ".{"
        "Type:Type,"
        "ReferenceLookupType:ReferenceLookupType,"
        "Description:Description"
        "}"
    )

    return query_info_output(options, LIST_LAYER_TYPES_QUERY, None, query)


@group.command(
    "describe-layer-type",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option("-t", "--type", required=True, help="The type of the layer to describe")
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def describe_layer_type(options, type, query):
    """
    Describes a specific layer type
    """
    DESCRIBE_LAYER_TYPE_QUERY = "LayerTypes[?Type=={type}] | [0]"

    click.echo(
        json.dumps(
            query_info_output(
                options, DESCRIBE_LAYER_TYPE_QUERY, {"type": type}, query
            ),
            indent=2,
        )
    )


@group.command(
    "query-layer-types", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def query_layer_types(options, query):
    """
    Query across all layer types
    """
    click.echo(
        json.dumps(query_info_output(options, "LayerTypes[]", None, query), indent=2)
    )


def layer_list_data_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Name"]),
                wrap_text(row["Id"]),
                wrap_text(row["Type"]),
                wrap_text(row["Active"]),
            ]
        )
    return tabulate(
        tablerows, headers=["Name", "Id", "Type", "Active"], tablefmt="github"
    )


@group.command(
    "list-layers", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="A query to filter out the results")
@json_or_table_option(layer_list_data_table)
@exceptions.backend_handler()
@pass_options
def list_layers(options, query):
    """
    Lists the layers available
    """

    LIST_LAYERS_QUERY = "LayerData[].{Name:Name,Id:Id,Type:Type,Active:Active}"

    return query_info_output(options, LIST_LAYERS_QUERY, {}, query)


@group.command(
    "describe-layer", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-t", "--type", required=True, help="The type of the layer to describe")
@click.option("-n", "--name", required=True, help="The name of the layer to describe")
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def describe_layer(options, type, name, query):
    """
    Describes a specific layer
    """
    DESCRIBE_LAYER_QUERY = "LayerData[?Type=={type} && Name=={name}] | [0]"

    click.echo(
        json.dumps(
            query_info_output(
                options, DESCRIBE_LAYER_QUERY, {"type": type, "name": name}, query
            ),
            indent=2,
        )
    )


@group.command(
    "query-layers", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="a query on the describe result")
@exceptions.backend_handler()
@pass_options
def query_layers(options, query):
    """
    Query across all layers
    """
    click.echo(
        json.dumps(query_info_output(options, "LayerData[]", None, query), indent=2)
    )
