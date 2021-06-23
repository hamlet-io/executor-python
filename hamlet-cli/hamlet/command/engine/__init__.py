import click
import os
import shutil
import json

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config
from hamlet.command.common.display import json_or_table_option, wrap_text

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.engine.engine_source import EngineSourceBuildData


def engines_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row['name']),
                wrap_text(row['description']),
                wrap_text(row['installed']),
                wrap_text(row['global']),
                wrap_text(row['update_available']),
            ]
        )
    return tabulate(
        tablerows,
        headers=['Name', 'Description', 'Installed', 'Global', 'Update Available'],
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

        update_available = None
        if engine.installed:
            if engine.up_to_date:
                update_available = False
            else:
                update_available = True

        data.append(
            {
                'name': engine.name,
                'description': engine.description,
                'installed': engine.installed,
                'digest': engine.digest,
                'global': True if engine.name == engine_store.global_engine else False,
                'update_available': update_available
            }
        )
    return data


@group.command(
    'describe-engine',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-n',
    '--name',
    help='An override to the default engine name to query'
)
@exceptions.backend_handler()
@config.pass_options
def describe_engine(opts, name):
    '''
    Provides a detailed description of an engine
    '''
    if name:
        engine_name = name
    elif opts.engine:
        engine_name = opts.engine
    else:
        engine_name = engine_store.global_engine

    engine = engine_store.get_engine(engine_name)

    engine_details = {
        'engine': {
            'name': engine.name,
            'description': engine.description,
            'hidden': engine.hidden,
            'installed': engine.installed,
            'engine_dir': engine.engine_dir,
            'up_to_date': engine.up_to_date,
            'current_digest': engine.digest,
            'latest_digest': engine.source_digest
        },
        'environment': engine.environment
    }

    sources = []
    for source in engine.sources:
        sources.append(
            {
                'name': source.name,
                'description': source.description,
                'latest_digest': source.digest,
                'build_details': source.build_details,
                'package_details': source.package_details
            }
        )

    parts = []
    for part in engine.parts:
        parts.append(
            {
                'type': part.type,
                'description': part.description,
                'source_path': part.source_path,
                'source_name': part.source_name
            }
        )

    engine_details['sources'] = sources
    engine_details['parts'] = parts

    click.echo(json.dumps(engine_details, indent=2))


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


@group.command(
    'env',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
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


@group.command(
    'add-engine-source-build',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-p',
    '--path',
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True
    ),
    default='.',
    help='The path to generate build details for'
)
@exceptions.backend_handler()
def add_engine_source_build(path):
    """
    Generates build metadata that will be used by the engine cli
    """
    build_details = EngineSourceBuildData(path=path)

    hamlet_meta_dir = os.path.join(path, '.hamlet')
    hamlet_build_state_file = os.path.join(hamlet_meta_dir, 'engine_source.json')
    if not os.path.isdir(hamlet_meta_dir):
        os.makedirs(hamlet_meta_dir)

    with open(hamlet_build_state_file, 'w') as file:
        json.dump(build_details.details, file, indent=2)
