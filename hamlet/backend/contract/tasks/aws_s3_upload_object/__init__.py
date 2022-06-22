import boto3


def run(
    BucketName,
    Object,
    LocalPath,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Upload an object from a local directory to an S3 Bucket
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    s3 = session.resource("s3")
    s3.Object(BucketName, Object).upload_file(LocalPath)

    return {
        "Properties": {
            "s3_path": f"s3://{BucketName}/{Object}",
            "local_path": LocalPath,
        }
    }
