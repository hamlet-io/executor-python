import click

from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options

from hamlet.backend.deploy import find_deployments, create_deployment


@click.command(
    "create-deployments", short_help="", context_settings=dict(max_content_width=240)
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
        [
            "deployed",
            "notdeployed",
        ],
        case_sensitive=False,
    ),
    default=["deployed", "notdeployed"],
    multiple=True,
    help="The states of deployments to include",
)
@click.option(
    "-d",
    "--district",
    default=["segment"],
    multiple=True,
    help="The districts to include deployments from",
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
@exceptions.backend_handler()
@pass_options
def create_deployments(
    options,
    deployment_mode,
    deployment_group,
    deployment_unit,
    deployment_state,
    output_dir,
    district,
    **kwargs,
):
    """
    Create deployment outputs
    """

    deployments = find_deployments(
        deployment_mode,
        deployment_group,
        deployment_units=deployment_unit,
        deployment_states=deployment_state,
        districts=district,
        **options.opts,
    )

    if len(deployments) == 0:
        raise exceptions.CommandError("No deployments found that match pattern")

    for deployment in deployments:

        deployment_group = deployment["DeploymentGroup"]
        deployment_unit = deployment["DeploymentUnit"]

        click.echo("")
        click.secho(f"[*] {deployment_group}/{deployment_unit}", bold=True, fg="green")
        click.echo("")

        create_deployment(
            deployment_group,
            deployment_unit,
            deployment_mode,
            output_dir,
            **options.opts,
        )
