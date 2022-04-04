import boto3
import os


def run(
    BucketName,
    Prefix,
    LocalPath,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Download the objects matching a prefix to a local directory from an S3 Bucket
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

    for object in bucket.objects.filter(Prefix=Prefix):
        object_count += 1
        local_path = os.path.join(
            os.path.abspath(LocalPath),
            object.key[len(os.path.commonpath([Prefix, object.key])) :],
        )

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        s3.Object(object.bucket_name, object.key).download_file(local_path)

    return {
        "Properties": {
            "object_count": str(object_count),
            "s3_path": f"s3://{BucketName}/" + Prefix,
            "local_path": LocalPath,
        }
    }
