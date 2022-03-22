import click
from tabulate import tabulate

from hamlet.command.common import config, exceptions
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.backend.deploy import find_deployments


def deployments_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["DeploymentGroup"]),
                wrap_text(row["DeploymentUnit"]),
                wrap_text(row["DeploymentProvider"]),
                wrap_text(row["CurrentState"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=[
            "Deployment Group",
            "Deployment Unit",
            "Provider",
            "State",
        ],
        tablefmt="github",
    )


@click.command(
    "list-deployments", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-m",
    "--deployment-mode",
    default="update",
    help="The deployment mode to use for the deployment",
)
@click.option(
    "-l",
    "--deployment-group",
    default=".*",
    show_default=True,
    help="The deployment group pattern to match",
)
@click.option(
    "-u",
    "--deployment-unit",
    default=[".*"],
    show_default=True,
    multiple=True,
    help="The deployment unit pattern to match",
)
@click.option(
    "-s",
    "--deployment-state",
    type=click.Choice(
        ["deployed", "notdeployed", "orphaned"],
        case_sensitive=False,
    ),
    default=["deployed", "notdeployed", "orphaned"],
    multiple=True,
    help="The states of deployments to include",
)
@json_or_table_option(deployments_table)
@exceptions.backend_handler()
@config.pass_options
def list_deployments(
    options,
    deployment_mode,
    deployment_group,
    deployment_unit,
    deployment_state,
):
    """
    List available deployments
    """
    return find_deployments(
        deployment_mode,
        deployment_group,
        deployment_units=deployment_unit,
        deployment_states=deployment_state,
        engine=options.engine,
        **options.opts,
    )
