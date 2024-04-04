import boto3


def run(
    StackName=None,
    ChangeSetName=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Return a list of all resources that will be changed
    """

    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )

    cfn = session.client("cloudformation")

    resource_modifications = [
        change
        for change in [
            change_list["ResourceChange"]
            for sublist in [
                x["Changes"]
                for x in cfn.get_paginator("describe_change_set").paginate(
                    ChangeSetName=ChangeSetName, StackName=StackName
                )
            ]
            for change_list in sublist
        ]
        if change["Action"] == "Modify"
    ]

    replacementResourceIds = [
        mod["LogicalResourceId"]
        for mod in resource_modifications
        if mod["Replacement"] in ["Conditional", "True"]
    ]

    return {
        "Properties": {
            "ReplacementResourceIds": replacementResourceIds,
            "ReplacementRequired": len(replacementResourceIds) > 0,
        }
    }
