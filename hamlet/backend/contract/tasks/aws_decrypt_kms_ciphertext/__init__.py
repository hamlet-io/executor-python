import boto3
from base64 import b64decode


def run(
    Ciphertext,
    Base64Encoded,
    EncryptionScheme,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Given an aws kms ciphertext blob decrypt it using the provided
    credentials and return the plaintext result as a string
    """

    if Base64Encoded is True:
        if EncryptionScheme != "":
            Ciphertext = Ciphertext.replace(EncryptionScheme, "", 1)
        Ciphertext = b64decode(Ciphertext)
    else:
        Ciphertext = bytes(Ciphertext)

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    kms = session.client("kms")
    result = kms.decrypt(
        CiphertextBlob=Ciphertext,
    )

    return {"Properties": {"result": result["Plaintext"].decode("utf-8")}}
