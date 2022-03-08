import json
from unittest import mock
from click.testing import CliRunner

from hamlet.command.engine import (
    list_engines,
    describe_engine,
    clean_engines,
    install_engine,
    set_engine,
    env,
)


def test_list_engines(options):
    cli = CliRunner()
    result = cli.invoke(list_engines, ["--output-format", "json"], obj=options)
    assert result.exit_code == 0
    print(result.output)
    result = json.loads(result.output)
    assert len(result) == 1
    assert {
        "name": "Name[1]",
        "description": "Description[1]",
        "digest": "Digest[1]",
        "short_digest": "Digest[1]",
        "location": "local",
    } in result


@mock.patch("json.dumps", mock.MagicMock(return_value="{}"))
def test_describe_engine(options):
    cli = CliRunner()
    result = cli.invoke(describe_engine, obj=options)
    print(result.exc_info)
    assert result.exit_code == 0


def test_install_engine(options):
    cli = CliRunner()
    result = cli.invoke(install_engine, ["engine[1]"], obj=options)
    print(result.exception)
    assert result.exit_code == 0


def test_env(options):
    cli = CliRunner()
    result = cli.invoke(env, [], obj=options)
    print(result.exception)
    assert result.exit_code == 0
    print(result.output)
    assert result.output == "# run eval $(hamlet engine env) to set variables\n"


def test_set_engine(options):
    cli = CliRunner()
    result = cli.invoke(set_engine, ["Name[1]"], obj=options)
    print(result.exception)
    assert result.exit_code == 0


def test_clean_engines(options):
    cli = CliRunner()
    result = cli.invoke(clean_engines, [], obj=options)
    print(result.exception)
    assert result.exit_code == 0
