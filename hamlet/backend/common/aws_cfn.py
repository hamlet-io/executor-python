from hamlet.backend.common.exceptions import BackendException


class CloudFormationStackException(BackendException):

    def __init__(self, stack_name, cfn_client, client_request_token):
        self.stack_name = stack_name

        stack_events = [
            "* "
            + " - ".join(
                [
                    stack_event["LogicalResourceId"],
                    stack_event["ResourceType"],
                    stack_event["ResourceStatus"],
                    stack_event.get("ResourceStatusReason", ""),
                ]
            )
            for sublist in [
                x["StackEvents"]
                for x in cfn_client.get_paginator("describe_stack_events").paginate(
                    StackName=self.stack_name
                )
            ]
            for stack_event in sublist
            if (
                stack_event.get("ClientRequestToken")
                and stack_event["ClientRequestToken"] == client_request_token
                and stack_event["ResourceStatus"]
                in [
                    "CREATE_FAILED",
                    "DELETE_FAILED",
                    "UPDATE_FAILED",
                    "UPDATE_ROLLBACK_FAILED",
                    "UPDATE_ROLLBACK_COMPLETE",
                    "ROLLBACK_FAILED",
                    "ROLLBACK_COMPLETE",
                ]
            )
        ]

        super().__init__(
            msg="Cloudformation failed to update the stack\n\n"
            + "\n".join(stack_events)
            + "\n"
        )
