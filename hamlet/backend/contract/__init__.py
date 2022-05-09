import importlib
import click
from hamlet.backend.contract.tasks.exceptions import (
    TaskConditionFailureException,
    TaskFailureException,
)


def run(contract, silent, engine, env):

    properties = contract["Properties"]

    for stage in contract["Stages"]:

        if not silent:
            click.echo(f"\n[-] Running contract stage {stage['Id']}")

        for step in stage["Steps"]:
            if not silent:
                click.echo(f"      Step: {step['Id']} - Task: {step['Type']}")

            try:
                task = importlib.import_module(
                    f"hamlet.backend.contract.tasks.{step['Type']}"
                )
            except ImportError as e:
                raise TaskFailureException(str(e))

            parameters = step["Parameters"]
            replaced_params = {}

            for k, v in parameters.items():
                replaced_params[k] = v
                if isinstance(v, str):
                    substitutions = v.split("__")
                    for substitution in substitutions:
                        if substitution.startswith("Properties:"):
                            property = substitution.split(":", 1)[1]

                            replacement_value = properties.get(property, "")
                            if isinstance(replacement_value, bool):
                                replaced_params[k] = replacement_value
                            else:
                                replaced_params[k] = replaced_params[k].replace(
                                    f"__Properties:{property}__",
                                    str(properties.get(property, "")),
                                )

            replaced_params["env"] = {**engine.environment, **env}
            try:
                task_result = task.run(**replaced_params)

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
