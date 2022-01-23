import boto3
from hamlet.backend.common import aws_ssm_session


def build_ssm_request_paramaters(task_details, container_name):
    cluster_name = task_details["clusterArn"].split("/")[-1]
    task_id = task_details["taskArn"].split("/")[-1]

    container_details = list(
        filter(
            lambda container: container["name"] == container_name,
            task_details["containers"],
        )
    )[0]

    ssm_request_params = {
        "Target": f"ecs:{cluster_name}_{task_id}_{container_details['runtimeId']}"
    }
    return ssm_request_params


def run(
    ClusterArn=None,
    TaskArn=None,
    ContainerName=None,
    Command=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Run an interactive command on aws ecs task
    Uses ECS SSM integration to provide interactive console through the
    Session Manager plugin for aws cli
    """
    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    ecs = session.client("ecs")

    execute_params = {
        "cluster": ClusterArn,
        "task": TaskArn,
        "command": Command,
        "interactive": True,
    }

    if ContainerName is not None:
        execute_params["container"] = ContainerName

    command = ecs.execute_command(**execute_params)

    task_details = ecs.describe_tasks(cluster=ClusterArn, tasks=[TaskArn])
    task_details = list(
        filter(lambda task: task["taskArn"] == TaskArn, task_details["tasks"])
    )[0]

    if ContainerName is None:
        ContainerName = task_details["containers"][0]["name"]

    aws_ssm_session.invoke(
        session_id=command["session"]["sessionId"],
        stream_url=command["session"]["streamUrl"],
        token_value=command["session"]["tokenValue"],
        parameters=build_ssm_request_paramaters(task_details, ContainerName),
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    return {"Properties": {}}
