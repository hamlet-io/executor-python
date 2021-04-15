import os
import re

from hamlet.backend import query as query_backend

LIST_DEPLOYMENTS_QUERY = (
    'Stages[].Steps[]'
    '.{'
    'DeploymentGroup:Parameters.DeploymentGroup,'
    'DeploymentUnit:Parameters.DeploymentUnit,'
    'DeploymentProvider:Parameters.DeploymentProvider,'
    'Operations:Parameters.Operations,'
    'CurrentState:Parameters.CurrentState'
    '}'
)


def find_deployments_from_options(
        options,
        deployment_mode,
        deployment_group,
        deployment_units,
        deployment_states=['deployed', 'notdeployed']):

    query_args = {
        **options.opts,
        'deployment_mode': deployment_mode,
        'generation_entrance': 'unitlist',
        'output_filename': 'unitlist-managementcontract.json',
        'use_cache': False,
    }
    available_deployments = query_backend.run(
        **query_args,
        cwd=os.getcwd(),
        query_text=LIST_DEPLOYMENTS_QUERY
    )

    deployments = []

    for deployment in available_deployments:
        if re.fullmatch(deployment_group, deployment['DeploymentGroup']):
            for deployment_unit in deployment_units:
                if re.fullmatch(deployment_unit, deployment['DeploymentUnit']):
                    if deployment['CurrentState'] in deployment_states:
                        deployments.append(deployment)

    return deployments
