import click
import os
import json
from tabulate import tabulate

from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command import root as cli
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options
from hamlet.backend import query as query_backend
from hamlet.backend import contract as contract_backend


def query_runbookinfo_state(options, query, query_params=None, sub_query_text=None):

    query_args = {
        **options.opts,
        "generation_entrance": "runbookinfo",
        "output_filename": "runbookinfo-config.json",
        "use_cache": False,
    }
    query_result = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=query,
        query_params=query_params,
        sub_query_text=sub_query_text,
    )

    return query_result


LIST_RUNBOOKS_QUERY = (
    "RunBooks[]" ".{" "Name:Name," "Description:Description," "Engine:Engine" "}"
)

DESCRIBE_RUNBOOK_QUERY = "RunBooks[?Name=={name}] | [0]"


def list_runbooks_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["Name"]),
                wrap_text(row["Description"]),
                wrap_text(row["Engine"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=[
            "Name",
            "Description",
            "Engine",
        ],
        tablefmt="github",
    )


@cli.group("task", context_settings=dict(max_content_width=240))
def group():
    """
    Runs tasks against a hamlet deployment
    """


@group.command(
    "list-runbooks", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-q", "--query", help="A JMESPath query to apply to the results")
@json_or_table_option(list_runbooks_table)
@exceptions.backend_handler()
@pass_options
def list_runbooks(options, query, **kwargs):
    """
    List available runbooks
    """
    return query_runbookinfo_state(
        options=options, query=LIST_RUNBOOKS_QUERY, sub_query_text=query
    )


@group.command(
    "describe-runbook", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-n", "--name", required=True, help="The name of the runbook to describe")
@click.option("-q", "--query", help="A JMESPath query to apply to the results")
@exceptions.backend_handler()
@pass_options
def describe_runbook(options, name, query=None, **kwargs):
    """
    Describe a specific runbook
    """

    result = query_runbookinfo_state(
        options=options,
        query=DESCRIBE_RUNBOOK_QUERY,
        query_params={"name": name},
        sub_query_text=query,
    )
    click.echo(json.dumps(result, indent=4))


@group.command(
    "run-runbook", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-n",
    "--name",
    required=True,
    help="The name of a runbook to execute",
)
@click.option(
    "--confirm/--no-confirm",
    default=False,
    help="Confirm before starting the runbook",
)
@click.argument("parameters", nargs=-1)
@exceptions.backend_handler()
@pass_options
def run_runbook(options, name, confirm, parameters, **kwargs):
    """
    Run a runbook
    """

    parameters = dict([arg.split("=") for arg in parameters])

    runbook_description = query_runbookinfo_state(
        options=options,
        query=DESCRIBE_RUNBOOK_QUERY,
        query_params={"name": name},
    )

    if runbook_description is None:
        raise exceptions.CommandError("No runbooks found with the provided name")

    click.echo("")
    click.secho(f"[*] {name}", bold=True, fg="green")
    if runbook_description["Description"] != "":
        click.secho(
            f"[*]   {runbook_description['Description']}", bold=True, fg="green"
        )
    click.echo("")

    if (confirm and click.confirm("Start Runbook?")) or not confirm:

        query_args = {
            **options.opts,
            "generation_entrance": "runbook",
            "generation_entrance_parameter": (
                f"RunBook={name}",
                f"RunBookInputs={json.dumps(parameters)}",
            ),
            "output_filename": "runbook-contract.json",
            "use_cache": False,
        }
        contract = query_backend.run(**query_args, cwd=os.getcwd(), query=None)
        contract_backend.run(contract)