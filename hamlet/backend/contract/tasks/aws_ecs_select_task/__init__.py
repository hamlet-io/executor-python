import boto3
from simple_term_menu import TerminalMenu
import json


def run(
    ClusterArn=None,
    TaskFamily=None,
    ServiceName=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Lists the available tasks for a given service or task definition
    Users select one and the result is returned
    """
    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    ecs = session.client("ecs")

    taskArns = []

    list_token = None
    while True:

        params = {
            "cluster": ClusterArn,
            "desiredStatus": "RUNNING",
        }

        if TaskFamily is not None:
            params["family"] = TaskFamily

        if ServiceName is not None:
            params["serviceName"] = ServiceName

        if list_token is not None:
            params["nextToken"] = list_token

        list_response = ecs.list_tasks(**params)
        taskArns += list_response["taskArns"]

        if list_response.get("nextToken", None) is not None:
            list_token = list_response["nextToken"]
        else:
            break

    task_details = ecs.describe_tasks(cluster=ClusterArn, tasks=taskArns)

    def get_task_preview(task_arn):

        task = list(
            filter(lambda task: task["taskArn"] == task_arn, task_details["tasks"])
        )[0]

        task_summary = {
            "containers": [
                {k: v for k, v in container.items() if k in ("name", "image")}
                for container in task["containers"]
            ],
            "startedAt": str(task["startedAt"]),
            "startedBy": task["startedBy"],
        }

        return json.dumps(task_summary, indent=2)

    menu = TerminalMenu(
        taskArns,
        title="Tasks",
        preview_command=get_task_preview,
        preview_title="details",
        preview_size=0.75,
    )

    print("\n")
    index = menu.show()
    task_arn = taskArns[index]

    print(f"Task Arn: {task_arn}")
    print("\n")

    return {"Properties": {"result": task_arn}}
