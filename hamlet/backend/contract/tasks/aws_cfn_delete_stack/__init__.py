import datetime

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
    Delete a CloudFormation Stack
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    client_request_token = str(int(datetime.datetime.now().timestamp()))

    cfn = session.client("cloudformation")
    cfn.delete_stack(
        StackName=StackName, ClientRequestToken=client_request_token,
    )

    cfn.get_waiter("stack_delete_complete").wait(StackName=StackName)

    return {"Properties": {}}
