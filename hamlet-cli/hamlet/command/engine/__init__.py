import click
import os
import shutil

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions
from hamlet.command.common import config

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME, ENGINE_STORE_DIR
from hamlet.command.common.display import json_or_table_option, wrap_text


def engines_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['name']),
                wrap_text(row['description']),
                wrap_text(row['installed']),
                wrap_text(row['global']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['Name', 'Description', 'Installed', 'GlobalEngine'],
        tablefmt='github'
    )


@cli.group('engine')
def group():
    """
    Manage the setup of your hamlet workspace
    """


@group.command(
    'list-engines',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@json_or_table_option(engines_table)
@exceptions.backend_handler()
def list_engines():
    '''
    Lists the available hamlet engines
    '''
    data = []

    for engine in engine_store.engines:
        data.append(
            {
                'name': engine.name,
                'description': engine.description,
                'installed': engine.installed,
                'digest': engine.digest,
                'global': True if engine.name == engine_store.global_engine else False
            }
        )
    return data


@group.command(
    'clean-engines',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@exceptions.backend_handler()
def clean_engines():
    '''
    Clean local engine store
    '''
    if os.path.isdir(ENGINE_STORE_DIR):
        shutil.rmtree(ENGINE_STORE_DIR)


@group.command(
    'install-engine',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-n',
    '--name',
    default='unicycle',
    show_default=True,
    help='The name of the engine to install'
)
@exceptions.backend_handler()
def install_engine(name):
    '''
    Get and install an hamlet engine version
    '''
    engine = engine_store.get_engine(name)
    engine.install()


@group.command(
    'set-engine',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.argument(
    'name',
    required=True,
    type=click.STRING
)
@exceptions.backend_handler()
def set_engine(name):
    '''
    sets the global default engine to use
    '''
    engine = engine_store.get_engine(name)

    if not engine.installed:
        engine.install()

    click.echo(f'default engine set to {name}')
    engine_store.global_engine = name


@group.command('env')
@click.argument(
    'environment_variable',
    required=False,
    type=click.STRING,
)
@click.option(
    '-n',
    '--engine-name',
    default=ENGINE_GLOBAL_NAME,
    show_default=True,
    help='The name of the engine to get env for'
)
@exceptions.backend_handler()
@config.pass_options
def env(options, environment_variable, engine_name):
    """
    Get the env variable config for hamlet
    """

    engine = engine_store.get_engine(engine_name)

    if environment_variable is None:
        click.echo('# run eval $(hamlet engine env) to set variables')
        for k, v in engine.environment.items():
            click.echo(f'export {k}="{v}"')

    else:
        try:
            click.echo(engine.environment[environment_variable])
        except KeyError:
            click.echo('')
