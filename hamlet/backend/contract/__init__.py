import importlib
from hamlet.backend.contract.tasks.exceptions import (
    TaskConditionFailureException,
    TaskFailureException,
)


def run(contract, **kwargs):

    properties = contract["Properties"]

    for stage in contract["Stages"]:

        print(f"[-] Running contract stage {stage['Id']}")

        for step in stage["Steps"]:
            print(f"      Step: {step['Id']} - Task: {step['Type']}")

            try:
                task = importlib.import_module(
                    f"hamlet.backend.contract.tasks.{step['Type']}"
                )
            except ImportError as e:
                raise TaskFailureException(str(e))

            parameters = step["Parameters"]

            for k, v in parameters.items():
                if isinstance(v, str):
                    substitutions = v.split("__")
                    for substitution in substitutions:
                        if substitution.startswith("Properties:"):
                            property = substitution.split(":", 1)[1]
                            parameters[k] = v.replace(
                                f"__Properties:{property}__",
                                properties.get(property, ""),
                            )

            parameters["env"] = kwargs
            try:
                task_result = task.run(**parameters)

                try:
                    for k, v in task_result["Properties"].items():
                        properties[f"output:{step['Id']}:{k}"] = v
                except KeyError:
                    pass

            except TaskConditionFailureException as e:
                if step["Status"] == "skip_stage_if_failure":
                    break
                else:
                    raise e

    contract["Properties"] = properties

    return contract
