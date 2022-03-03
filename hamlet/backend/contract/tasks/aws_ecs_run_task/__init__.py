import json
import boto3
import click

from botocore.exceptions import WaiterError
from hamlet.backend.common.utilities import to_bool


def run(
    ClusterArn=None,
    TaskFamily=None,
    CapacityProvider=None,
    SubnetIds=None,
    SecurityGroupIds=None,
    PublicIP=None,
    ShowStatus=None,
    WaitToStop=None,
    OverrideContainerName=None,
    CommandOverride=None,
    EnvironmentOverrides=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Start a new task using the provided TaskFamily
    with any overrides applied to a given container
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )
    ecs = session.client("ecs")

    network_config = None

    if SubnetIds is not None and SecurityGroupIds is not None:
        network_config = {
            "awsvpcConfiguration": {
                "subnets": SubnetIds.split(","),
                "securityGroups": SecurityGroupIds.split(","),
                "assignPublicIp": "ENABLED" if to_bool(PublicIP, False) else "DISABLED",
            }
        }

    container_override = None
    if OverrideContainerName is not None and (
        CommandOverride is not None or EnvironmentOverrides is not None
    ):
        container_override = {"name": OverrideContainerName}

        if CommandOverride is not None:

            try:
                command = json.loads(CommandOverride)
            except json.decoder.JSONDecodeError:
                command = [CommandOverride]

            if isinstance(command, str):
                command = [command]

            container_override["command"] = command

        if EnvironmentOverrides is not None:
            container_override["environment"] = [
                {"name": key, "value": value}
                for key, value in json.loads(EnvironmentOverrides).items()
            ]

    overrides = None
    if container_override is not None:
        overrides = {"containerOverrides": [container_override]}

    task_response = ecs.run_task(
        cluster=ClusterArn,
        taskDefinition=TaskFamily,
        capacityProviderStrategy=[
            {
                "capacityProvider": CapacityProvider,
            }
        ],
        count=1,
        enableECSManagedTags=True,
        propagateTags="TASK_DEFINITION",
        networkConfiguration=network_config,
        overrides=overrides,
    )

    task_args = {
        "cluster": ClusterArn,
        "tasks": [task["taskArn"] for task in task_response["tasks"]],
    }

    if to_bool(ShowStatus, True):
        click.echo("waiting for task to start", err=True)

    try:
        running_waiter = ecs.get_waiter("tasks_running")
        running_waiter.wait(**task_args)

    except WaiterError:
        if True in [
            True
            for task in ecs.describe_tasks(**task_args)["tasks"]
            if task["lastStatus"] == "STOPPED"
        ]:
            pass

    if to_bool(WaitToStop, True):

        if to_bool(ShowStatus, True):
            click.echo("waiting for task to stop", err=True)

        stopped_waiter = ecs.get_waiter("tasks_stopped")
        stopped_waiter.wait(**task_args)

    if to_bool(ShowStatus, True):
        task_describe = ecs.describe_tasks(**task_args)
        run_status = {"tasks": []}

        try:
            run_status["failures"] = task_describe["failures"]
        except KeyError:
            pass

        task_keys = [
            "stopCode",
            "stoppedReason",
            "taskArn",
            "lastStatus",
            "capacityProviderName",
        ]
        container_keys = [
            "name",
            "image",
            "runtimeId",
            "lastStatus",
            "exitCode",
            "reason",
        ]

        for task in task_describe["tasks"]:
            task_status = {k: v for k, v in task.items() if k in task_keys}

            task_status["startedAt"] = task["startedAt"].isoformat()
            task_status["stoppedAt"] = task["stoppedAt"].isoformat()

            task_status["containers"] = []
            for container in task["containers"]:
                task_status["containers"].append(
                    {k: v for k, v in container.items() if k in container_keys}
                )

            run_status["tasks"].append(task_status)

        click.echo(json.dumps(run_status, indent=2))

    return {
        "Properties": {
            "task_arns": [task["taskArn"] for task in task_response["tasks"]],
        }
    }
