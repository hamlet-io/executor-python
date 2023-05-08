import json
import boto3

from botocore.exceptions import WaiterError
from hamlet.backend.common.utilities import to_bool
from hamlet.backend.common.exceptions import BackendException


def run(
    ClusterArn=None,
    TaskFamily=None,
    ContainerName=None,
    CapacityProvider=None,
    SubnetIds=None,
    SecurityGroupIds=None,
    PublicIP=None,
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

    run_task_args = {
        "cluster": ClusterArn,
        "taskDefinition": TaskFamily,
        "capacityProviderStrategy": [
            {
                "capacityProvider": CapacityProvider,
            }
        ],
        "count": 1,
        "enableECSManagedTags": True,
        "propagateTags": "TASK_DEFINITION",
    }

    if SubnetIds and SecurityGroupIds:
        run_task_args["networkConfiguration"] = {
            "awsvpcConfiguration": {
                "subnets": SubnetIds.split(","),
                "securityGroups": SecurityGroupIds.split(","),
                "assignPublicIp": "ENABLED" if to_bool(PublicIP, False) else "DISABLED",
            }
        }

    if CommandOverride or EnvironmentOverrides:
        container_override = {"name": ContainerName}

        if CommandOverride:
            try:
                command = json.loads(CommandOverride)
            except json.decoder.JSONDecodeError:
                command = [CommandOverride]

            if isinstance(command, str):
                command = [command.split(" ")]

            container_override["command"] = command

        if EnvironmentOverrides:
            container_override["environment"] = [
                {"name": key, "value": value}
                for key, value in json.loads(EnvironmentOverrides).items()
            ]

        run_task_args["overrides"] = {"containerOverrides": [container_override]}

    task_response = ecs.run_task(**run_task_args)

    task_args = {
        "cluster": ClusterArn,
        "tasks": [task["taskArn"] for task in task_response["tasks"]],
    }

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

    while True:
        try:
            stopped_waiter = ecs.get_waiter("tasks_stopped")
            stopped_waiter.wait(**task_args)
        except WaiterError:
            continue

        break

    task_describe = ecs.describe_tasks(**task_args)
    run_status = {"tasks": []}

    if task_describe.get("failures", None):
        raise BackendException(task_describe["failures"])

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
            if container["name"] == ContainerName and container["exitCode"] != 0:
                raise BackendException(
                    (
                        "Primary container did not run successfully "
                        f"- exitCode: {container['exitCode']}"
                    )
                )

        run_status["tasks"].append(task_status)

    return {
        "Properties": {
            "task_arns": json.dumps(
                [task["taskArn"] for task in task_response["tasks"]]
            ),
            "run_status": json.dumps(run_status),
        }
    }
