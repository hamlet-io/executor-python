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


def find_schemas_from_options(options, schema):
    query_args = {
        **options.opts,
        "deployment_mode": None,
        "generation_entrance": "schemalist",
        "output_filename": "schemalist-schemacontract.json",
        "use_cache": False,
    }
    available_schemas = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        engine=options.engine,
        query_text=LIST_SCHEMAS_QUERY,
    )

    schemas = []

    for available_schema in available_schemas:
        if re.fullmatch(schema, available_schema["Schema"]):
            schemas.append(available_schema)
    return schemas


@cli.group("schema", context_settings=dict(max_content_width=240))
def group():
    """
    Generates JSONSchemas for Hamlet Configuration Scopes
    """
    pass


LIST_SCHEMAS_QUERY = "Stages[].Steps[]" ".{" "Schema:Parameters.Schema" "}"


def schema_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Schema"]),
            ]
        )
    return tabulate(tablerows, headers=["Schema"], tablefmt="github")


@group.command(
    "list-schemas", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-s",
    "--schema",
    default=".*",
    show_default=True,
    help="A schema name pattern to filter results",
)
@json_or_table_option(schema_table)
@exceptions.backend_handler()
@pass_options
def list_schemas(options, schema):
    """
    List the available JSONSchemas that can be created
    """

    return find_schemas_from_options(options, schema)


@group.command(
    "create-schemas", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-s",
    "--schema",
    default=".*",
    show_default=True,
    help="A schema name pattern to filter the schemas that will be generated",
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
def create_schemas(options, schema, output_dir, **kwargs):
    """
    Create the JSON schema files available
    """

    schema_list = find_schemas_from_options(options, schema)

    if len(schema_list) == 0:
        raise exceptions.CommandError("No schemas found")

    for schema_task in schema_list:
        click.echo("")
        click.echo(
            (
                click.style(
                    f"[*] Schema: {schema_task['Schema']}",
                    bold=True,
                    fg="green",
                )
            )
        )
        click.echo("")

        template_args = {
            **options.opts,
            "entrance": "schema",
            "output_dir": output_dir,
            "entrance_parameter": f"Schema={schema_task['Schema']}",
        }

        create_template_backend.run(
            **template_args, engine=options.engine, _is_cli=True
        )
