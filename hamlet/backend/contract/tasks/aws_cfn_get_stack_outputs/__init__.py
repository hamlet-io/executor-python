import boto3


def run(
    StackName=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
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

    return {"Properties": {"Outputs": stack_outputs}}
