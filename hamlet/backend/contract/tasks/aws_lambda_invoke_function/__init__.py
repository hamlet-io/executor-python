from hamlet.backend.common.exceptions import BackendException
import boto3


def run(
    FunctionArn,
    Payload,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Invoke a lambda function synchronously and wait for the result
    Fail on lambda error and return logs and result
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    lambda_client = session.client("lambda")
    result = lambda_client.invoke(
        FunctionName=FunctionArn,
        InvocationType="RequestResponse",
        LogType="None",
        Payload=bytes(Payload, "utf-8"),
    )

    if "FunctionError" in result:
        raise BackendException(
            f"Lambda Function Failure - {result['FunctionError']} - {result['Payload'].read().decode('utf-8')}"
        )

    return {"Properties": {"payload": result["Payload"].read().decode("utf-8")}}
