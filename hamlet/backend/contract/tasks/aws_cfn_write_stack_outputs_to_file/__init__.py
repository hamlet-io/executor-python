import json

import boto3


def run(
    StackName=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    FilePath=None,
    env={},
):
    """
    Return the outputs of a stack
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")
    stack_response = cfn.describe_stacks(StackName=StackName)

    try:
        stack_outputs = [
            stack
            for stack in stack_response["Stacks"]
            if stack["StackStatus"]
            not in [
                "CREATE_FAILED",
                "DELETE_COMPLETE",
            ]
        ][0]["Outputs"]
    except IndexError:
        stack_outputs = []

    if stack_outputs:
        with open(FilePath, "w") as f:
            f.write(json.dumps({"Stacks": [{"Outputs": stack_outputs}]}, indent=2))

    return {"Properties": {"Outputs": stack_outputs}}
