import os
import re

from hamlet.backend import query as query_backend
from hamlet.backend.manage import stack as manage_stack_backend
from hamlet.backend.manage import deployment as manage_deployment_backend
from hamlet.backend.create import template as create_template_backend
from hamlet.backend.common.exceptions import BackendException


class UnsupportedDeploymentProviderException(BackendException):
    def __init__(self, deployment_provider, message):
        self.deployment_provider = deployment_provider
        super.__init__(message=message)


LIST_DEPLOYMENTS_QUERY = (
    "Stages[].Steps[]"
    ".{"
    "DeploymentGroup:Parameters.DeploymentGroup,"
    "DeploymentUnit:Parameters.DeploymentUnit,"
    "DeploymentProvider:Parameters.DeploymentProvider,"
    "Operations:Parameters.Operations,"
    "CurrentState:Parameters.CurrentState"
    "}"
)


def find_deployments(
    deployment_mode,
    deployment_group,
    deployment_units,
    engine,
    deployment_states=["deployed", "notdeployed"],
    **kwargs,
):
    query_args = {
        **kwargs,
        "deployment_mode": deployment_mode,
        "generation_entrance": "unitlist",
        "output_filename": "unitlist-managementcontract.json",
    }
    available_deployments = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=LIST_DEPLOYMENTS_QUERY,
        engine=engine,
    )

    deployments = []

    for deployment in available_deployments:
        if re.fullmatch(deployment_group, deployment["DeploymentGroup"]):
            for deployment_unit in deployment_units:
                if re.fullmatch(deployment_unit, deployment["DeploymentUnit"]):
                    if deployment["CurrentState"] in deployment_states:
                        deployments.append(deployment)

    return deployments


def create_deployment(
    deployment_group,
    deployment_unit,
    deployment_mode,
    output_dir,
    engine,
    _is_cli=True,
    **kwargs,
):
    generate_args = {
        **kwargs,
        "entrance": "deployment",
        "deployment_group": deployment_group,
        "deployment_unit": deployment_unit,
        "deployment_mode": deployment_mode,
        "output_dir": output_dir,
    }
    create_template_backend.run(**generate_args, engine=engine, _is_cli=_is_cli)


def run_deployment(
    deployment_provider,
    deployment_group,
    deployment_unit,
    operation,
    output_dir,
    engine,
    dryrun=False,
    **kwargs,
):
    manage_args = {
        "deployment_group": deployment_group,
        "deployment_unit": deployment_unit,
        "output_dir": output_dir,
        "dryrun": dryrun,
        **kwargs,
    }

    if operation == "delete":
        manage_args["delete"] = True

    if deployment_provider == "aws":
        manage_stack_backend.run(**manage_args, engine=engine, _is_cli=True)

    elif deployment_provider == "azure":
        manage_deployment_backend.run(**manage_args, engine=engine, _is_cli=True)

    else:
        raise UnsupportedDeploymentProviderException(
            f"Deployment provider {deployment_provider} is not supported",
            deployment_provider=deployment_provider,
        )
