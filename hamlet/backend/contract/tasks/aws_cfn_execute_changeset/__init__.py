import boto3
from hamlet.backend.common.exceptions import BackendException

CFN_FAILURE_EVENTS = [
    "CREATE_FAILED",
    "UPDATE_FAILED",
    "IMPORT_FAILED",
    "IMPORT_ROLLBACK_FAILED",
    "UPDATE_ROLLBACK_FAILED",
    "ROLLBACK_FAILED",
    "DELETE_FAILED",
]


def run(
    StackName=None,
    ChangeSetName=None,
    RunId=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Execute a CloudFormation ChangeSet
    """

    client_request_token = f"hamlet_{ChangeSetName}_{RunId}"

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")

    stack_in_review = any(
        [
            stack["StackName"] == StackName
            for sublist in [
                x["StackSummaries"]
                for x in cfn.get_paginator("list_stacks").paginate(
                    StackStatusFilter="REVIEW_IN_PROGRESS"
                )
            ]
            for stack in sublist
        ]
    )

    cfn.execute_change_set(
        ChangeSetName=ChangeSetName,
        StackName=StackName,
        ClientRequestToken=client_request_token,
    )

    if stack_in_review:
        cfn.get_waiter("stack_create_complete").wait(StackName=StackName)
    else:
        cfn.get_waiter("stack_update_complete").wait(StackName=StackName)

    stack = cfn.describe_stacks(StackName=StackName)["Stacks"][0]

    if stack["StackStatus"] in CFN_FAILURE_EVENTS:
        failed_stack_events = [
            event
            for sublist in [
                x["StackEvents"]
                for x in cfn.get_paginator("describe_stack_events").paginate(
                    StackName=StackName
                )
            ]
            for event in sublist
            if event["ClientRequestToken"] == client_request_token
            and event["ResourceStatus"] in CFN_FAILURE_EVENTS
        ]
        exception_msg_str = "\n".join(
            [
                f"{event['LogicalResourceId']} - {event['ResourceStatus']} - {event['ResourceStatusReason']}"
                for event in failed_stack_events
            ]
        )

        raise BackendException(
            f"Issues occurred executing the ChangeSet\nResource Events:\n{exception_msg_str}"
        )

    return {
        "Properties": {
            "Status": stack["StackStatus"],
            "Outputs": {x["OutputKey"]: x["OutputValue"] for x in stack["Outputs"]},
        }
    }
