import json
from unittest import mock
from click.testing import CliRunner


from hamlet.command.engine import (
    list_engines,
    clean_engines,
    install_engine,
    set_engine,
    env
)


def mock_engine(name, description, installed, digest=''):
    mock_engine = mock.Mock()
    mock_engine.name = name
    mock_engine.description = description
    mock_engine.digest = digest
    type(mock_engine).installed = mock.PropertyMock(return_value=installed)

    return mock_engine


def mock_backend():
    def decorator(func):
        @mock.patch('hamlet.command.engine.engine_store')
        def wrapper(mock_engine_store, *args, **kwargs):

            mock_engines = [
                mock_engine(
                    name='Name[1]',
                    description='Description[1]',
                    installed=False
                ),
                mock_engine(
                    name='Name[2]',
                    description='Description[2]',
                    installed=True,
                    digest='Digest[2]'
                )
            ]

            type(mock_engine_store).engines = mock.PropertyMock(return_value=mock_engines)
            type(mock_engine_store).global_engine = mock.PropertyMock(return_value='Name[2]')

            return func(mock_engine_store, *args, **kwargs)

        return wrapper
    return decorator


@mock_backend()
def test_list_engines(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(
        list_engines,
        [
            '--output-format', 'json'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    print(result)
    assert len(result) == 2
    assert {
        'name': 'Name[1]',
        'description': 'Description[1]',
        'digest': '',
        'installed': False,
        'global': False,
    } in result
    assert {
        'name': 'Name[2]',
        'description': 'Description[2]',
        'digest': 'Digest[2]',
        'installed': True,
        'global': True,
    } in result


@mock_backend()
def test_install_engine(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(
        install_engine,
        [
            'engine[1]'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0


@mock_backend()
def test_env(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(
        env,
        []
    )
    print(result.exception)
    assert result.exit_code == 0
    print(result.output)
    assert result.output == '# run eval $(hamlet engine env) to set variables\n'


@mock_backend()
def test_set_engine(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(
        set_engine,
        [
            'Name[1]'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0


@mock_backend()
def test_clean_engines(mock_engine_store):
    cli = CliRunner()
    result = cli.invoke(
        clean_engines,
        []
    )
    print(result.exception)
    assert result.exit_code == 0
