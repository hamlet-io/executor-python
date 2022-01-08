import boto3
from simple_term_menu import TerminalMenu
import json


def run(
    Tags=None,
    VpcId=None,
    Region=None,
    AWSAccessKeyId=None,
    AWSSecretAccessKey=None,
    AWSSessionToken=None,
    env={},
):
    """
    Lists the available ec2 instances using a vpc or tag based filter
    Users select one and the returned result is the ec2 instance id
    """
    session = boto3.Session(
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretAccessKey,
        aws_session_token=AWSSessionToken,
        region_name=Region,
    )
    ec2 = session.resource("ec2")

    filters = []

    if VpcId is not None:
        filters.append({"Name": "vpc-id", "Values": [VpcId]})

    if Tags is not None:
        for k, v in Tags.items():
            filters.append({"Name": f"tag:{k}", "Values": [v]})

    ec2_instances = ec2.instances.filter(Filters=filters)
    instance_ids = [instance.id for instance in ec2_instances]

    def get_instance_preview(instance_id):
        instance = ec2.Instance(instance_id)
        task_summary = {
            "Name": [tag["Value"] for tag in instance.tags if tag["Key"] == "Name"][0],
            "State": instance.state["Name"],
            "PrivateIp": instance.private_ip_address,
            "Type": instance.instance_type,
            "LaunchTime": str(instance.launch_time),
        }

        return json.dumps(task_summary, indent=2)

    menu = TerminalMenu(
        instance_ids,
        title="EC2 Instances",
        preview_command=get_instance_preview,
        preview_title="details",
        preview_size=0.75,
    )

    print("\n")
    index = menu.show()
    instance_id = instance_ids[index]

    print(f"Instance Id: {instance_id}")
    print("\n")

    return {"Properties": {"result": instance_id}}
