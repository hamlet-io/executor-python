import boto3


def run(
    StackName=None,
    RunId=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Delete a CloudFormation Stack
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")
    cfn.delete_stack(
        StackName=StackName, ClientRequestToken=f"hamlet_{StackName}_{RunId}"
    )

    cfn.get_waiter("stack_delete_complete").wait(StackName=StackName)

    return {"Properties": {}}
