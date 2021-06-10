import click
import os
import shutil

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
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
    Manage the engine used by the executor
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
    Lists the available engines
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

    if os.path.isdir(engine_store.store_dir):
        shutil.rmtree(engine_store.store_dir)


@group.command(
    'install-engine',
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
def install_engine(name):
    '''
    Install an engine
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
    Sets the global engine used
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
@exceptions.backend_handler()
@config.pass_options
def env(opts, environment_variable):
    """
    Get the environment variables for the current engine
    """

    if opts.engine is None:
        engine = engine_store.get_engine(ENGINE_GLOBAL_NAME)
    else:
        engine = engine_store.get_engine(opts.engine)

    if environment_variable is None:
        click.echo('# run eval $(hamlet engine env) to set variables')
        for k, v in engine.environment.items():
            click.echo(f'export {k}="{v}"')

    else:
        try:
            click.echo(engine.environment[environment_variable])
        except KeyError:
            click.echo('')
