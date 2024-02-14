import datetime
from typing import Optional

import boto3
import botocore


def run(
    TemplateS3Uri=None,
    TemplateBody=None,
    StackName=None,
    ChangeSetName=None,
    Parameters=None,
    Capabilities: Optional[str] = None,
    Region: Optional[str] = None,
    AWSAccessKeyId: Optional[str] = None,
    AWSSecretAccessKey: Optional[str] = None,
    AWSSessionToken: Optional[str] = None,
    env={},
):
    """
    Create a CloudFormation ChangeSet
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")

    client_token = str(int(datetime.datetime.now().timestamp()))

    existing_stacks = [
        stack
        for sublist in [
            x["StackSummaries"] for x in cfn.get_paginator("list_stacks").paginate()
        ]
        for stack in sublist
        if stack["StackName"] == StackName
    ]

    for stack in [
        stack for stack in existing_stacks if stack["StackStatus"] == "CREATE_FAIlED"
    ]:
        cfn.delete_stack(StackName=stack["StackName"])
        cfn.get_waiter("stack_delete_complete").wait(StackName=stack["StackName"])

    change_set_params = {
        "StackName": StackName,
        "ChangeSetName": ChangeSetName,
        "ChangeSetType": "CREATE",
        "ClientToken": client_token,
    }

    if TemplateS3Uri:
        change_set_params["TemplateURL"] = TemplateS3Uri
    elif TemplateBody:
        change_set_params["TemplateBody"] = TemplateBody

    if (
        len(
            [
                stack
                for stack in existing_stacks
                if stack["StackStatus"] not in ["DELETE_COMPLETE", "CREATE_FAILED"]
            ]
        )
        > 0
    ):
        change_set_params["ChangeSetType"] = "UPDATE"

    if Parameters:
        change_set_params["Parameters"] = [
            {"ParameterKey": k, "ParameterValue": v} for k, v in Parameters.items()
        ]

    if Capabilities:
        change_set_params["Capabilities"] = Capabilities.split(",")

    cfn.create_change_set(**change_set_params)
    changes_required = True

    try:
        cfn.get_waiter("change_set_create_complete").wait(
            ChangeSetName=ChangeSetName,
            StackName=StackName,
        )
    except botocore.exceptions.WaiterError as error:
        change_set_state = cfn.describe_change_set(
            ChangeSetName=ChangeSetName,
            StackName=StackName
        )
        if (
            change_set_state["Status"] == "FAILED"
            and change_set_state["StatusReason"] == "The submitted information didn't contain changes. Submit different information to create a change set."
        ):
            changes_required = False
        else:
            raise error

    return {
        "Properties": {
            "changes_required": str(changes_required)
        }
    }
