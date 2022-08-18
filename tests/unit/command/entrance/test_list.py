import os
import json
from unittest import mock
from click.testing import CliRunner
from hamlet.command.entrance import list_entrances as list_entrances


def template_backend_run_mock(data):
    def run(output_filename="info.json", output_dir=None, *args, **kwargs):
        os.makedirs(output_dir, exist_ok=True)
        info_filename = os.path.join(output_dir, output_filename)
        with open(info_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(info=None):
    def decorator(func):
        @mock.patch("hamlet.backend.query.template")
        def wrapper(blueprint_mock, *args, **kwargs):
            blueprint_mock.run.side_effect = template_backend_run_mock(info)

            return func(blueprint_mock, *args, **kwargs)

        return wrapper

    return decorator


@mock_backend(
    {
        "Entrances": [
            {"Type": "EntranceType[1]", "Description": "EntranceDescription[1]"},
            {"Type": "EntranceType[2]", "Description": "EntranceDescription[2]"},
        ]
    }
)
def test_query_list_entrances(blueprint_mock):
    cli = CliRunner()
    result = cli.invoke(list_entrances, ["--output-format", "json"])
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        "Type": "EntranceType[1]",
        "Description": "EntranceDescription[1]",
    } in result
    assert {
        "Type": "EntranceType[2]",
        "Description": "EntranceDescription[2]",
    } in result
