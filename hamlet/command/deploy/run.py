import click
from hamlet.command.common import config, exceptions
from hamlet.backend.deploy import find_deployments, create_deployment, run_deployment


@click.command(
    "run-deployments", short_help="", context_settings=dict(max_content_width=240)
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
            "orphaned",
        ],
        case_sensitive=False,
    ),
    default=["deployed", "notdeployed"],
    multiple=True,
    help="The states of deployments to include",
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
    help="the directory where the outputs will be saved",
)
@click.option(
    "--refresh-outputs/--no-refresh-outputs",
    default=True,
    help="Update outputs or use existing",
)
@click.option(
    "--confirm/--no-confirm",
    default=False,
    help="Confirm before executing each deployment",
)
@click.option(
    "--dryrun/--no-dryrun",
    default=False,
    help="Perform a dry run of the deployment before the run",
)
@exceptions.backend_handler()
@config.pass_options
def run_deployments(
    options,
    deployment_mode,
    deployment_group,
    deployment_unit,
    deployment_state,
    output_dir,
    refresh_outputs,
    confirm,
    dryrun,
    **kwargs,
):
    """
    Create and run deployments
    """
    deployments = find_deployments(
        deployment_mode,
        deployment_group,
        deployment_units=deployment_unit,
        deployment_states=deployment_state,
        engine=options.engine,
        **options.opts,
    )

    if len(deployments) == 0:
        raise exceptions.CommandError("No deployments found that match pattern")

    for deployment in deployments:

        deployment_group = deployment["DeploymentGroup"]
        deployment_unit = deployment["DeploymentUnit"]
        deployment_state = deployment["CurrentState"]
        provider = deployment["DeploymentProvider"]

        click.echo("")
        click.secho(f"[*] {deployment_group}/{deployment_unit}", bold=True, fg="green")

        if deployment_state == "orphaned":
            click.secho(
                "[-] deployment has been orphaned, running orphan clean up",
                bold=False,
                fg="yellow",
            )

        click.echo("")

        if refresh_outputs:
            if deployment_state != "orphaned":
                create_deployment(
                    deployment_group=deployment_group,
                    deployment_unit=deployment_unit,
                    deployment_mode=deployment_mode,
                    output_dir=output_dir,
                    engine=options.engine,
                    **options.opts,
                )

        for operation in deployment["Operations"]:

            if dryrun:
                run_deployment(
                    deployment_provider=provider,
                    deployment_group=deployment_group,
                    deployment_unit=deployment_unit,
                    operation=operation,
                    output_dir=output_dir,
                    dryrun=dryrun,
                    engine=options.engine,
                    **options.opts,
                )

            if (
                confirm
                and click.confirm(
                    f"Start Deployment of {deployment_group}/{deployment_unit} ?"
                )
            ) or not confirm:
                run_deployment(
                    deployment_provider=provider,
                    deployment_group=deployment_group,
                    deployment_unit=deployment_unit,
                    operation=operation,
                    output_dir=output_dir,
                    engine=options.engine,
                    **options.opts,
                )
