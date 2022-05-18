import boto3
import json
import jmespath


def run(
    SecretArn,
    JSONKeyPath,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Retrieve the value of secrets manager secret
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    secretsmanager = session.client("secretsmanager")
    secret_response = secretsmanager.get_secret_value(SecretId=SecretArn)

    try:
        secret_value = json.loads(secret_response["SecretString"])
        secret_value = jmespath.search(JSONKeyPath, secret_value)

    except json.JSONDecodeError:
        secret_value = secret_response["SecretString"]

    return {"Properties": {"secret_value": secret_value}}
