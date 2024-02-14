import boto3


def run(
    BucketName,
    Object,
    ClientMethod,
    Expiration,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Return a presigned url for an object in a bucket
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    s3 = session.client("s3")
    presigned_url = s3.generate_presigned_url(
        ClientMethod=ClientMethod,
        Params={
            "Bucket": BucketName,
            "Key": Object
        },
        ExpiresIn=Expiration
    )

    return {
        "Properties": {
            "presigned_url": presigned_url
        }
    }
