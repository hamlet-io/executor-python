import os
import hashlib
import json
import tempfile
from unittest import mock
from click.testing import CliRunner

from hamlet.command.component.describe_occurrence import describe_occurrence
from hamlet.command.component.list_occurrences import list_occurrences
from hamlet.command.component.query_occurrences import query_occurrences

from hamlet.command.component.common import DescribeContext


def template_backend_run_mock(data):
    def run(
        entrance="occurrences",
        entrance_parameter=None,
        output_filename="occurrences-state.json",
        output_dir=None,
        deployment_mode=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        log_level=None,
        district_type=None,
        root_dir=None,
        tenant=None,
        account=None,
        product=None,
        environment=None,
        segment=None,
        engine=None,
    ):
        os.makedirs(output_dir, exist_ok=True)
        blueprint_filename = os.path.join(output_dir, output_filename)
        with open(blueprint_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(blueprint=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.context.Context")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, ContextClassMock, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(
                    hashlib.md5(str(blueprint).encode()).hexdigest()
                )
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(blueprint)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

        return wrapper

    return decorator


def mock_describe_context(name=None):
    def decorator(func):
        @mock.patch.object(DescribeContext, "name", name)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


occurrence_state_data = {
    "Occurrences": [
        {
            "Core": {
                "Tier": {"Id": "TierId[1]"},
                "Component": {"Id": "ComponentId[1]", "RawId": "ComponentRawId[1]"},
                "TypedRawName": "CoreRawName[1]",
                "Type": "CoreType[1]",
            },
            "Configuration": {
                "Solution": {"deployment:Unit": "DeploymentUnit[1]"},
                "SettingNamespaces": [{"Key": "SettingNamespace[1]"}],
            },
            "State": {
                "Resources": {
                    "Resource[1]": {"Id": "ResourceId[1]", "Name": "ResourceName[1]"}
                },
                "Attributes": {"ATTRIBUTE[1]": "AttributeValue[1]"},
            },
        },
        {
            "Core": {
                "Tier": {"Id": "TierId[2]"},
                "Component": {"Id": "ComponentId[2]", "RawId": "ComponentRawId[2]"},
                "TypedRawName": "CoreRawName[2]",
                "Type": "CoreType[2]",
            },
            "Configuration": {
                "Solution": {"deployment:Unit": "DeploymentUnit[2]"},
                "SettingNamespaces": [{"Key": "SettingNamespace[2]"}],
            },
            "State": {
                "Resources": {
                    "Resource[1]": {"Id": "ResourceId[2]", "Name": "ResourceName[2]"}
                },
                "Attributes": {"ATTRIBUTE[1]": "AttributeValue[2]"},
            },
        },
    ]
}


@mock_backend(occurrence_state_data)
def test_list_occurrences(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(list_occurrences, ["--output-format", "json"])
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    print(result)
    assert len(result) == 2
    assert {
        "TierId": "TierId[1]",
        "ComponentId": "ComponentRawId[1]",
        "Name": "CoreRawName[1]",
        "Type": "CoreType[1]",
    } in result
    assert {
        "TierId": "TierId[2]",
        "ComponentId": "ComponentRawId[2]",
        "Name": "CoreRawName[2]",
        "Type": "CoreType[2]",
    } in result


@mock_describe_context("CoreRawName[1]")
@mock_backend(occurrence_state_data)
def test_describe_occurrence(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(describe_occurrence, ["--name", "CoreRawName[1]"])
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == occurrence_state_data["Occurrences"][0]


@mock_describe_context("CoreRawName[1]")
@mock_backend(occurrence_state_data)
def test_describe_occurrence_query(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(
        describe_occurrence,
        ["--name", "CoreRawName[1]", "--query", "Configuration.Solution"],
    )
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {"deployment:Unit": "DeploymentUnit[1]"}


@mock_describe_context("CoreRawName[1]")
@mock_backend(occurrence_state_data)
def test_describe_occurrence_query_solution(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(describe_occurrence, ["--name", "CoreRawName[1]", "solution"])
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {"deployment:Unit": "DeploymentUnit[1]"}


@mock_describe_context("CoreRawName[1]")
@mock_backend(occurrence_state_data)
def test_describe_occurrence_query_resources(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(describe_occurrence, ["--name", "CoreRawName[1]", "resources"])
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {
        "Resource[1]": {"Id": "ResourceId[1]", "Name": "ResourceName[1]"}
    }


@mock_describe_context("CoreRawName[1]")
@mock_backend(occurrence_state_data)
def test_describe_occurrence_query_setting_namespaces(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(
        describe_occurrence, ["--name", "CoreRawName[1]", "setting-namespaces"]
    )
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == [{"Key": "SettingNamespace[1]"}]


@mock_describe_context("CoreRawName[1]")
@mock_backend(occurrence_state_data)
def test_describe_occurrence_query_attributes(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(
        describe_occurrence,
        [
            "--name",
            "CoreRawName[1]",
            "attributes",
            "--output-format",
            "json",
        ],
    )
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {"ATTRIBUTE[1]": "AttributeValue[1]"}


@mock_backend(occurrence_state_data)
def test_query_occurrences(blueprint_mock, ContextClassMock):

    cli = CliRunner()
    result = cli.invoke(
        query_occurrences,
        [
            "--query",
            "Occurrences[0].{ComponentId:Core.Component.Id}",
        ],
    )

    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {"ComponentId": "ComponentId[1]"}
