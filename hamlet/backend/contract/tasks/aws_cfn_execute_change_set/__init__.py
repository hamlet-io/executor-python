import datetime

import boto3
import botocore

from hamlet.backend.common.aws_cfn import CloudFormationStackException


def run(
    StackName=None,
    ChangeSetName=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Execute a CloudFormation ChangeSet
    """
    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")
    client_request_token = str(int(datetime.datetime.now().timestamp()))

    stack_in_review = any(
        [
            stack["StackName"] == StackName
            for sublist in [
                x["StackSummaries"]
                for x in cfn.get_paginator("list_stacks").paginate(
                    StackStatusFilter=["REVIEW_IN_PROGRESS"]
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

    try:
        if stack_in_review:
            cfn.get_waiter("stack_create_complete").wait(StackName=StackName)
        else:
            cfn.get_waiter("stack_update_complete").wait(StackName=StackName)

    except botocore.exceptions.WaiterError as error:
        if error.last_response["Stacks"][0]["StackStatus"] in [
            "UPDATE_ROLLBACK_FAILED",
            "UPDATE_ROLLBACK_COMPLETE",
            "UPDATE_FAILED",
            "CREATE_FAILED",
        ]:
            raise CloudFormationStackException(StackName, cfn, client_request_token)

    return {"Properties": {}}
