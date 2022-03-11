import os
import click


from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options
from hamlet.command.common.validate import validate_entrance_inputs
from hamlet.backend.create import template as create_template_backend
from hamlet.backend import query as query_backend


@cli.group("entrance", context_settings=dict(max_content_width=240))
def group():
    """
    Hamlet entrances provide access to the hamlet cmdb to perform different tasks
    """
    pass


LIST_ENTRANCES_QUERY = "Entrances[].{Type:Type,Description:Description}"


def entrances_table(data):
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
        showindex=True,
        tablefmt="fancy_grid",
    )


@group.command(
    "list-entrances", short_help="", context_settings=dict(max_content_width=240)
)
@json_or_table_option(entrances_table)
@exceptions.backend_handler()
@pass_options
def list_entrances(options):
    """
    List available entrances
    """
    args = {
        **options.opts,
        "generation_input_source": "mock",
        "generation_entrance": "info",
        "output_filename": "info.json",
        "use_cache": False,
    }

    return query_backend.run(
        **args, cwd=os.getcwd(), query_text=LIST_ENTRANCES_QUERY, engine=options.engine
    )


@group.command(
    "invoke-entrance", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-e",
    "--entrance",
    help="The entrance to invoke for output generation",
    required=True,
)
@click.option(
    "-y",
    "--entrance-parameter",
    multiple=True,
    help="key=value pairs that are passed to to the entrance",
    callback=validate_entrance_inputs,
)
@click.option(
    "-l",
    "--deployment-group",
    help="deployment group the deployment unit belongs to",
)
@click.option(
    "-u",
    "--deployment-unit",
    help="deployment unit to be included in the template",
)
@click.option(
    "-z", "--deployment-unit-subset", help="subset of the deployment unit required"
)
@click.option(
    "-d",
    "--deployment-mode",
    help="deployment mode the template will be generated for",
    default="update",
    show_default=True,
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
    help="the directory where the outputs will be saved. Mandatory when input source is set to mock",
)
@click.option(
    "-x",
    "--disable-output-cleanup",
    is_flag=True,
    help="disable the cleanup of the output directory before generation",
)
@click.option(
    "-c",
    "--config-ref",
    help="identifier of the configuration used to generate this template",
    default="unassigned",
    show_default=True,
)
@click.option(
    "-q",
    "--request-ref",
    help="opaque value to link this template to a triggering request management system",
    default="unassigned",
    show_default=True,
)
@exceptions.backend_handler()
@pass_options
def invoke_entrance(options, **kwargs):
    """
    Invoke a Hamlet Entrance
    """
    args = {**options.opts, **kwargs}

    create_template_backend.run(**args, engine=options.engine, _is_cli=True)
