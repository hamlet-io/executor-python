from hamlet.backend.contract.tasks.exceptions import TaskConditionFailureException


def run(Condition, Test, Value, env={}):
    """
    Conditional testing service to handle skipping steps in a contract
    """
    result = False

    if Condition == "Equals":
        result = Test == Value
    elif Condition == "StartsWith":
        result = Value.startswith(Test)
    elif Condition == "EndsWith":
        result = Value.endswith(Test)
    elif Condition == "Contains":
        result = Value.contains(Test)

    if not result:
        raise TaskConditionFailureException("Condition not met")

    return {"Properties": {"result": result}}
