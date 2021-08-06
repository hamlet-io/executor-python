import click
import os
import json

from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config
from hamlet.command.common.display import json_or_table_option, wrap_text
from hamlet.command.common.config import pass_options

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.engine.engine_code_source import EngineCodeSourceBuildData
from hamlet.backend.engine.exceptions import (
    HamletEngineInvalidVersion,
    EngineStoreMissingEngineException,
)


def engines_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["name"]),
                wrap_text(row["description"]),
                wrap_text(row["installed"]),
                wrap_text(row["global"]),
                wrap_text(row["update_available"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=["Name", "Description", "Installed", "Global", "Update Available"],
        tablefmt="github",
    )


@cli.group("engine", context_settings=dict(max_content_width=240))
def group():
    """
    Manage the engine used by the executor
    """


@group.command(
    "list-engines", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "--show-hidden/--hide-hidden",
    default=False,
    help="Control visibility of hidden engines",
)
@json_or_table_option(engines_table)
@exceptions.backend_handler()
def list_engines(show_hidden):
    """
    Lists the available engines
    """
    data = []

    for engine in engine_store.find_engines(cache_timeout=0):

        update_available = None
        if (show_hidden and engine.hidden) or not engine.hidden:
            if engine.installed:
                try:
                    if engine.up_to_date():
                        update_available = False
                    else:
                        update_available = True
                except BaseException as e:
                    click.secho(
                        f"[!]engine update failed for {engine.name}", fg="red", err=True
                    )
                    click.secho(f"[!]  {e}", fg="red", err=True)

            data.append(
                {
                    "name": engine.name,
                    "description": engine.description,
                    "installed": engine.installed,
                    "digest": engine.digest,
                    "global": True
                    if engine.name == engine_store.global_engine
                    else False,
                    "update_available": update_available,
                }
            )
    return data


@group.command(
    "describe-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.argument("name", required=False, type=click.STRING)
@exceptions.backend_handler()
@config.pass_options
def describe_engine(opts, name):
    """
    Provides a detailed description of an engine
    """
    if name:
        engine_name = name
    elif opts.engine:
        engine_name = opts.engine
    else:
        engine_name = engine_store.global_engine

    engine = engine_store.find_engine(engine_name)

    try:

        up_to_date = engine.up_to_date()
        latest_digest = engine.get_latest_digest()

    except BaseException as e:
        click.secho(
            f"[!] Engine update check failed for {engine.name}", fg="red", err=True
        )
        click.secho(f"[!]  {e}", fg="red", err=True)

        up_to_date = None
        latest_digest = None
        pass

    engine_details = {
        "engine": {
            "name": engine.name,
            "description": engine.description,
            "hidden": engine.hidden,
            "installed": engine.installed,
            "engine_dir": engine.engine_dir,
            "up_to_date": up_to_date,
            "current_digest": engine.digest,
            "latest_digest": latest_digest,
        },
        "environment": engine.environment,
        "install_state": engine.install_state,
    }

    sources = []
    for source in engine.sources:

        try:
            source_digest = source.digest
        except BaseException as e:
            click.secho(
                f"[!] Source check failed {engine.name} - {source.name}",
                fg="red",
                err=True,
            )
            click.secho(f"[!]  {e}", fg="red", err=True)

            source_digest = None
            pass

        sources.append(
            {
                "name": source.name,
                "description": source.description,
                "latest_digest": source_digest,
            }
        )

    parts = []
    for part in engine.parts:
        parts.append(
            {
                "type": part.type,
                "description": part.description,
                "source_path": part.source_path,
                "source_name": part.source_name,
            }
        )

    engine_details["sources"] = sources
    engine_details["parts"] = parts

    click.echo(json.dumps(engine_details, indent=2))


@group.command(
    "clean-engines", short_help="", context_settings=dict(max_content_width=240)
)
@click.argument("name", type=click.STRING, nargs=-1)
@exceptions.backend_handler()
def clean_engines(name):
    """
    Clean local engine store
    """
    if name:
        for engine in name:
            click.echo(f"[*] cleaning {engine} from {engine_store.store_dir}")
            engine_store.clean_engine(engine)

    else:
        click.echo(f"[*] cleaning all engines from {engine_store.store_dir}")
        engine_store.clean_engines()


@group.command(
    "install-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-u",
    "--update",
    is_flag=True,
    help="Update the engine",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Force reinstall of engine",
)
@click.argument("name", required=False, type=click.STRING)
@exceptions.backend_handler()
@pass_options
def install_engine(opts, name, force, update):
    """
    Install an engine
    """

    if name is None:
        name = opts.engine or engine_store.global_engine

    try:
        engine = engine_store.find_engine(name, cache_timeout=0)

    except HamletEngineInvalidVersion as e:
        click.secho(
            (
                "[!] The state of this engine is not compatible with the cli\n"
                f"[!] Remove the engine using\n"
                f"     hamlet engine clean-engine {name}\n"
                "[!] then install the engine again"
            ),
            err=True,
            fg="red",
        )
        raise e

    if not engine.installed or force:
        click.echo(
            f"[*] installing engine | {name} | digest: {engine.get_latest_digest()}"
        )
        engine.install()
    elif not engine.up_to_date() and update:
        click.echo(f"[*] updating engine | {name}")
        click.echo(
            f"[*] current digest: {engine.digest} | latest digest: {engine.get_latest_digest()}"
        )
        engine.install()
    else:
        click.echo(f"[*] engine installed | {name} | digest: {engine.digest}")


@group.command(
    "set-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.argument("name", required=False, type=click.STRING)
@exceptions.backend_handler()
@config.pass_options
def set_engine(opts, name):
    """
    Sets the global engine used
    """
    name = name or opts.engine

    try:
        engine = engine_store.get_engine(name)

    except EngineStoreMissingEngineException:

        engine = engine_store.find_engine(name, cache_timeout=0)

        if not engine.installed:
            click.echo("[*] installing engine")
            engine.install()

    click.echo(f"[*] global engine set to {name}")
    engine_store.global_engine = name


@group.command(
    "get-engine", short_help="", context_settings=dict(max_content_width=240)
)
@exceptions.backend_handler()
@config.pass_options
def get_engine(opts):
    """
    Gets the current global engine
    """
    name = opts.engine or engine_store.global_engine
    click.echo(engine_store.get_engine(name).name)


@group.command("env", short_help="", context_settings=dict(max_content_width=240))
@click.argument(
    "environment_variable",
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
        click.echo("# run eval $(hamlet engine env) to set variables")
        for k, v in engine.environment.items():
            click.echo(f'export {k}="{v}"')

    else:
        try:
            click.echo(engine.environment[environment_variable])
        except KeyError:
            click.echo("")


@group.command(
    "add-engine-source-build",
    short_help="",
    context_settings=dict(max_content_width=240),
)
@click.option(
    "-p",
    "--path",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True
    ),
    default=".",
    help="The path to generate build details for",
)
@exceptions.backend_handler()
def add_engine_source_build(path):
    """
    Generates build metadata for engine sources
    """

    build_details = EngineCodeSourceBuildData(path=path)

    hamlet_meta_dir = os.path.join(path, ".hamlet")
    hamlet_build_state_file = os.path.join(hamlet_meta_dir, "engine_source.json")
    if not os.path.isdir(hamlet_meta_dir):
        os.makedirs(hamlet_meta_dir)

    with open(hamlet_build_state_file, "w") as file:
        json.dump(build_details.details, file, indent=2)
