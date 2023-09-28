import boto3


def run(
    ResourceIds=None,
    StackName=None,
    ChangeSetName=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Check to see if a given set of resource Ids are going to be replaced
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")

    resource_modifications = [
        change["ResourceChange"]
        for sublist in [
            x["Changes"]
            for x in cfn.get_paginator("describe_change_set").paginate(
                ChangeSetName=ChangeSetName, StackName=StackName
            )
        ]
        for change in sublist
        if change["ResourceType"] == "ResourceType"
        and change["ResourceChange"] == "Modify"
    ]

    replacementResourceIds = [
        mod["LogicalResourceId"]
        for mod in resource_modifications
        if mod["Replacement"] in ["Conditonally", "Always"]
        and (mod["LogicalResourceId"] in ResourceIds or ResourceIds is None)
    ]

    return {
        "Properties": {
            "ReplacementResourceIds": replacementResourceIds,
            "ReplacementRequired": len(replacementResourceIds) > 0,
        }
    }
