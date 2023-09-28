import boto3


def run(
    TemplateS3Uri=None,
    StackName=None,
    ChangeSetName=None,
    RunId=None,
    Parameters=None,
    Capabilities=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
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

    existing_stacks = [
        stack
        for sublist in [
            x["StackSummaries"] for x in cfn.get_paginator("list_stacks").paginate()
        ]
        for stack in sublist
        if stack["StackName"] == StackName
    ]

    for stack in [
        stack for stack in existing_stacks if stack["StackState"] == "CREATE_FAIlED"
    ]:
        cfn.delete_stack(StackName=stack["StackName"])
        cfn.get_waiter("stack_delete_complete").wait(StackName=stack["StackName"])

    change_set_params = {
        "StackName": StackName,
        "ChangeSetName": ChangeSetName,
        "TemplateURL": TemplateS3Uri,
        "ChangeSetType": "CREATE",
        "ClientToken": f"hamlet_{ChangeSetName}_{RunId}",
    }

    if (
        len(
            [
                stack
                for stack in existing_stacks
                if stack["StackState"] not in ["DELETE_COMPLETE", "CREATE_FAILED"]
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
        change_set_params["Capabilities"] = Capabilities

    change_set_response = cfn.create_change_set(**change_set_params)
    cfn.get_waiter("change_set_create_complete").wait(
        ChangeSetName=ChangeSetName,
        StackName=StackName,
    )

    return {"Properties": change_set_response}
