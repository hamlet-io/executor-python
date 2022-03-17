import os
import tempfile
import click

from hamlet.command.common import config, exceptions
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.test.generate import run as test_generate_backend
from hamlet.backend.test import run as test_run_backend
from hamlet.backend.deploy import find_deployments, create_deployment


@click.command(
    "test-deployments", short_help="", context_settings=dict(max_content_width=240)
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
    "-o",
    "--output-dir",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    help="The directory where tests are run - temp dir by default",
)
@click.option(
    "-p", "--pytest-args", "pytest_args", help="additional arguments for pytest"
)
@click.option("-s", "--silent", "silent", is_flag=True, help="minimize pytest output")
@exceptions.backend_handler()
@config.pass_options
def test_deployments(
    options,
    deployment_mode,
    deployment_group,
    deployment_unit,
    output_dir,
    pytest_args,
    silent,
    **kwargs,
):
    """
    Create deployments and test them using their test cases
    """
    temp_dir = None

    if output_dir is None:
        temp_dir = tempfile.TemporaryDirectory()
        output_dir = temp_dir.name

    output_dir = os.path.abspath(output_dir)

    deployments = find_deployments(
        deployment_mode=deployment_mode,
        deployment_group=deployment_group,
        deployment_units=deployment_unit,
        engine=options.engine,
        **options.opts,
    )

    if len(deployments) == 0:
        raise exceptions.CommandError("No deployments found that match pattern")

    click.echo("")
    click.echo(click.style("[*] Creating deployments:", bold=True, fg="green"))
    click.echo("")
    for deployment in deployments:

        deployment_group = deployment["DeploymentGroup"]
        deployment_unit = deployment["DeploymentUnit"]

        click.echo(f"[-] {deployment_group}/{deployment_unit}")

        create_deployment(
            deployment_group,
            deployment_unit,
            deployment_mode,
            output_dir,
            _is_cli=False,
            engine=options.engine,
            **options.opts,
        )

        generate_args = {
            **options.opts,
            "entrance": "deploymenttest",
            "deployment_group": deployment_group,
            "deployment_unit": deployment_unit,
            "deployment_mode": deployment_mode,
            "output_dir": output_dir,
        }
        create_template_backend.run(
            **generate_args, engine=options.engine, _is_cli=False
        )

    click.echo("")
    click.secho("[*] Testing deployments:", bold=True, fg="green")
    click.echo("")

    test_script_filename = "test_deployments.py"
    test_generate_backend(
        output=f"{output_dir}/{test_script_filename}",
        directory=output_dir,
    )

    try:
        test_run_backend.run(
            testpaths=[test_script_filename],
            pytest_args=pytest_args,
            silent=silent,
            root_dir=output_dir,
        )
    except Exception as e:
        raise exceptions.CommandError(str(e))
