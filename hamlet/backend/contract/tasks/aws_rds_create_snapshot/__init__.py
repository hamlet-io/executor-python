import boto3
import datetime

from hamlet.backend.common.utilities import to_bool


def get_tag_set(dbArn, rds_client):
    return [
        tag
        for tag in rds_client.list_tags_for_resource(ResourceName=dbArn)["TagList"]
        if not tag["Key"].startswith("rds:") and not tag["Key"].startswith("aws:")
    ]


def run(
    DbId=None,
    Cluster=None,
    SnapshotName=None,
    IncludeDateSuffix=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Create a manual snapshot of an RDS instance or cluster
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )
    rds = session.client("rds")

    SnapshotName = (
        f"{SnapshotName}-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}"
        if to_bool(IncludeDateSuffix, True)
        else SnapshotName
    )

    if to_bool(Cluster, False):
        cluster = rds.describe_db_clusters(DBClusterIdentifier=DbId)

        snapshot_response = rds.create_db_cluster_snapshot(
            DBClusterSnapshotIdentifier=SnapshotName,
            DBClusterIdentifier=DbId,
            Tags=get_tag_set(cluster["DBClusters"][0]["DBClusterArn"], rds),
        )

        waiter = rds.get_waiter("db_cluster_snapshot_available")
        waiter.wait(
            DBClusterSnapshotIdentifier=SnapshotName,
            DBClusterIdentifier=DbId,
            SnapshotType="manual",
        )
        snapshot_arn = snapshot_response["DBClusterSnapshot"]["DBClusterSnapshotArn"]

    else:
        instance = rds.describe_db_instances(DBInstanceIdentifier=DbId)

        snapshot_response = rds.create_db_snapshot(
            DBSnapshotIdentifier=SnapshotName,
            DBInstanceIdentifier=DbId,
            Tags=get_tag_set(instance["DBInstances"][0]["DBInstanceArn"], rds),
        )

        waiter = rds.get_waiter("db_snapshot_completed")
        waiter.wait(
            DBSnapshotIdentifier=SnapshotName,
            DBInstanceIdentifier=DbId,
            SnapshotType="manual",
        )

        snapshot_arn = snapshot_response["DBSnapshot"]["DBSnapshotArn"]

    return {"Properties": {"SnapshotArn": snapshot_arn}}
