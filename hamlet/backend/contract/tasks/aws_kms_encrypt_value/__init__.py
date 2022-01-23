import boto3
from base64 import b64encode


def run(
    KeyArn,
    Value,
    EncryptionScheme="",
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Given a string use aws kms to encrypt the string and return the value
    as a base64 encoded string of the ciphertext blog as the result
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    kms = session.client("kms")
    result = kms.encrypt(
        KeyId=KeyArn,
        Plaintext=bytes(Value, "utf-8"),
    )

    return {
        "Properties": {
            "result": f"{EncryptionScheme}{b64encode(result['CiphertextBlob']).decode('utf-8')}"
        }
    }
