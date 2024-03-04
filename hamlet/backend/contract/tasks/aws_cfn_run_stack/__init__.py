import datetime
from typing import Optional

import boto3
import botocore

from hamlet.backend.common.aws_cfn import CloudFormationStackException


def run(
    TemplateS3Uri=None,
    TemplateBody=None,
    StackName=None,
    Parameters=None,
    Capabilities: Optional[str] = None,
    Region: Optional[str] = None,
    AWSAccessKeyId: Optional[str] = None,
    AWSSecretAccessKey: Optional[str] = None,
    AWSSessionToken: Optional[str] = None,
    env={},
):
    """
    Create or Update a Cloudformation stack
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")

    client_request_token = str(int(datetime.datetime.now().timestamp()))

    # Setup the parameters for what goes in the stack deployment
    stack_params = {
        "StackName": StackName,
        "ClientRequestToken": client_request_token,
    }

    if TemplateS3Uri:
        stack_params["TemplateURL"] = TemplateS3Uri
    elif TemplateBody:
        stack_params["TemplateBody"] = TemplateBody

    if Parameters:
        stack_params["Parameters"] = [
            {"ParameterKey": k, "ParameterValue": v} for k, v in Parameters.items()
        ]

    if Capabilities:
        stack_params["Capabilities"] = Capabilities.split(",")

    # remove any stacks that failed create
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

        try:
            cfn.get_waiter("stack_delete_complete").wait(StackName=stack["StackName"])
        except botocore.exceptions.WaiterError as error:
            if error.last_response["Stacks"][0]["StackStatus"] in [
                "DELETE_FAILED",
            ]:
                raise CloudFormationStackException(StackName, cfn, client_request_token)

    # Handle the switch between create and update
    if len(existing_stacks) == 0 or all(stack["StackStatus"] in ["CREATE_FAILED", "DELETE_COMPLETE"] for stack in existing_stacks):
        cfn.create_stack(**stack_params)

        try:
            cfn.get_waiter("stack_create_complete").wait(
                StackName=StackName,
            )

        except botocore.exceptions.WaiterError as error:
            if error.last_response["Stacks"][0]["StackStatus"] in [
                "CREATE_FAILED",
            ]:
                raise CloudFormationStackException(StackName, cfn, client_request_token)

    else:
        try:
            cfn.update_stack(**stack_params)
        except botocore.exceptions.ClientError as error:
            if (
                error.response["Error"]["Code"] == "ValidationError"
                and error.response["Error"]["Message"] == "No updates are to be performed."
            ):
                return {
                    "Properties": {}
                }
            else:
                raise error

        try:
            cfn.get_waiter("stack_update_complete").wait(
                StackName=StackName
            )
        except botocore.exceptions.WaiterError as error:
            if error.last_response["Stacks"][0]["StackStatus"] in [
                "UPDATE_ROLLBACK_FAILED",
                "UPDATE_ROLLBACK_COMPLETE",
                "UPDATE_FAILED",
            ]:
                raise CloudFormationStackException(StackName, cfn, client_request_token)

    return {
        "Properties": {}
    }
