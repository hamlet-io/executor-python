import json
from unittest import mock

from click.testing import CliRunner

from hamlet.command.engine import (
    clean_engines,
    describe_engine,
    install_engine,
    list_engines,
    set_engine,
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
