import boto3


def run(
    BucketName,
    Prefix,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Remove all objects from an S3 bucket prefix
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    s3 = session.resource("s3")
    bucket = s3.Bucket(BucketName)
    object_count = 0

    if bucket.Versioning().status in ["Enabled", "Suspended"]:
        for object in bucket.object_versions.filter(Prefix=Prefix):
            object_count += 1
            object.delete()

    else:
        for object in bucket.objects.filter(Prefix=Prefix):
            object_count += 1
            object.delete()

    return {
        "Properties": {
            "object_count": str(object_count),
            "s3_path": f"s3://{BucketName}/" + Prefix,
        }
    }
