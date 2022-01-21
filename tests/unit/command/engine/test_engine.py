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


def mock_engine(name, description, location, digest=""):
    mock_engine = mock.Mock()
    mock_engine.name = name
    mock_engine.description = description
    mock_engine.digest = digest
    mock_engine.short_digest = digest
    mock_engine.location = location

    return mock_engine


def mock_backend():
    def decorator(func):
        @mock.patch("hamlet.command.engine.engine_store")
        def wrapper(mock_engine_store, *args, **kwargs):

            mock_engines = [
                mock_engine(
                    name="Name[1]",
                    description="Description[1]",
                    digest="Digest[1]",
                    location="local",
                ),
            ]
            mock_engine_store.get_engines.return_value = mock_engines

            return func(mock_engine_store, *args, **kwargs)

        return wrapper

    return decorator


@mock_backend()
def test_list_engines(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(list_engines, ["--output-format", "json"])
    assert result.exit_code == 0
    result = json.loads(result.output)
    print(result)
    assert len(result) == 1
    assert {
        "name": "Name[1]",
        "description": "Description[1]",
        "digest": "Digest[1]",
        "short_digest": "Digest[1]",
        "location": "local",
    } in result


@mock.patch("json.dumps", mock.MagicMock(return_value="{}"))
@mock_backend()
def test_describe_engine(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(describe_engine)
    print(result.output)
    assert result.exit_code == 0


@mock_backend()
def test_install_engine(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(install_engine, ["engine[1]"])
    print(result.exception)
    assert result.exit_code == 0


@mock_backend()
def test_env(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(env, [])
    print(result.exception)
    assert result.exit_code == 0
    print(result.output)
    assert result.output == "# run eval $(hamlet engine env) to set variables\n"


@mock_backend()
def test_set_engine(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(set_engine, ["Name[1]"])
    print(result.exception)
    assert result.exit_code == 0


@mock_backend()
def test_clean_engines(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(clean_engines, [])
    print(result.exception)
    assert result.exit_code == 0
