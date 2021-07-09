import os
import re
import click

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options
from hamlet.backend import query as query_backend
from hamlet.backend.create import template as create_template_backend


def find_schemas_from_options(options, schema_type, schema_instances):
    query_args = {
        **options.opts,
        "deployment_mode": None,
        "generation_entrance": "schemaset",
        "output_filename": "schemaset-schemacontract.json",
        "use_cache": False,
    }
    available_schemas = query_backend.run(
        **query_args, cwd=os.getcwd(), query_text=LIST_SCHEMAS_QUERY
    )

    schemas = []

    for schema in available_schemas:
        if re.fullmatch(schema_type, schema["SchemaType"]):
            for schema_instance in schema_instances:
                if re.fullmatch(schema_instance, schema["SchemaInstance"]):
                    schemas.append(schema)
    return schemas


@cli.group("schema", context_settings=dict(max_content_width=240))
def group():
    """
    Generates JSONSchema files for Hamlet data types
    """
    pass


LIST_SCHEMAS_QUERY = (
    "Stages[].Steps[]"
    ".{"
    "SchemaType:Parameters.SchemaType,"
    "SchemaInstance:Parameters.SchemaInstance"
    "}"
)


def schema_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["SchemaType"]),
                wrap_text(row["SchemaInstance"]),
            ]
        )
    return tabulate(
        tablerows, headers=["SchemaType", "SchemaInstance"], tablefmt="github"
    )


@group.command(
    "list-schemas", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-t",
    "--schema-type",
    default=".*",
    show_default=True,
    help="A schema type name pattern to filter results",
)
@click.option(
    "-i",
    "--schema-instance",
    default=[".*"],
    show_default=True,
    multiple=True,
    help="A schema instance name pattern to filter results",
)
@json_or_table_option(schema_table)
@exceptions.backend_handler()
@pass_options
def list_schemas(options, schema_type, schema_instance):
    """
    List the available JSON schemas by data type
    """

    return find_schemas_from_options(options, schema_type, schema_instance)


@group.command(
    "create-schemas", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-t",
    "--schema-type",
    default=".*",
    show_default=True,
    help="A schema type name pattern to filter results",
)
@click.option(
    "-i",
    "--schema-instance",
    default=[".*"],
    show_default=True,
    multiple=True,
    help="A schema instance name pattern to filter results",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    required=True,
    help="the directory where the outputs will be saved",
)
@exceptions.backend_handler()
@pass_options
def create_schemas(options, schema_type, schema_instance, output_dir, **kwargs):
    """
    Create Hamlet data type schemas
    """

    schemas = find_schemas_from_options(options, schema_type, schema_instance)

    if len(schemas) == 0:
        raise exceptions.CommandError("No schemas found")

    for schema in schemas:
        schema_type = schema["SchemaType"]
        schema_instance = schema["SchemaInstance"]
        click.echo("")
        click.echo(
            (
                click.style(
                    f"[*] Schema: {schema_type}/{schema_instance}",
                    bold=True,
                    fg="green",
                )
            )
        )
        click.echo("")

        template_args = {
            **options.opts,
            "entrance": "schema",
            "deployment_group": schema_type,
            "deployment_unit": schema_instance,
            "output_dir": output_dir,
        }

        create_template_backend.run(**template_args, _is_cli=True)
