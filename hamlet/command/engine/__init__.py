import click
import os
import json
from tabulate import tabulate

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config
from hamlet.command.common.display import json_or_table_option, wrap_text

from hamlet.backend.engine import engine_store
from hamlet.backend.engine.common import ENGINE_GLOBAL_NAME
from hamlet.backend.engine.engine_code_source import EngineCodeSourceBuildData
from hamlet.backend.engine.exceptions import (
    HamletEngineInvalidVersion,
    EngineStoreMissingEngineException,
)


def engine_locations_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["name"]),
                wrap_text(row["description"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=["Name", "Description"],
        tablefmt="github",
    )


def engines_table(data):
    tablerows = []
    for row in data:
        tablerows.append(
            [
                wrap_text(row["name"]),
                wrap_text(row["location"]),
                wrap_text(row["description"]),
                wrap_text(row["short_digest"]),
            ]
        )
    return tabulate(
        tablerows,
        headers=["Name", "Location", "Description", "Short Digest"],
        tablefmt="github",
    )


@cli.group("engine", context_settings=dict(max_content_width=240))
def group():
    """
    Manage the engine used by the executor
    """
    pass


@group.command(
    "list-engine-locations", short_help="", context_settings=dict(max_content_width=240)
)
@json_or_table_option(engine_locations_table)
@exceptions.backend_handler()
def list_engine_locations():
    """
    Lists the engine locations
    """
    data = []
    for k, location in engine_store.engine_locations.items():
        data.append(
            {
                "name": k,
                "description": location["description"],
            }
        )

    return data


@group.command(
    "list-engines", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-l",
    "--location",
    multiple=True,
    help="The location of the engine to look for the engine",
    default=["installed", "local", "remote"],
)
@json_or_table_option(engines_table)
@exceptions.backend_handler()
def list_engines(location):
    """
    Lists the engines available
    """

    engine_store.load_engines(locations=location, refresh=True)
    data = []
    for engine in engine_store.get_engines(locations=location):
        data.append(
            {
                "name": engine.name,
                "location": engine.location,
                "description": engine.description,
                "short_digest": engine.short_digest,
                "digest": engine.digest,
            }
        )

    return data


@group.command(
    "describe-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.option("-l", "--location", help="The location of the engine to describe")
@click.argument("name", required=False, type=click.STRING)
@exceptions.backend_handler()
@config.pass_options
def describe_engine(opts, name, location):
    """
    Provides a detailed description of an engine
    """

    location = None if not location else [location]

    if name:
        engine_name = name

    elif opts.engine:
        engine_name = opts.engine
        location = ["installed"]
    else:
        engine_name = engine_store.global_engine
        location = ["installed"]

    engine_store.load_engines(locations=location, refresh=True)
    engines = [
        engine
        for engine in engine_store.get_engines(locations=location)
        if engine.name == engine_name
    ]
    if len(engines) > 1:

        extra_engines = "\n".join(
            [
                f" - name: {engine.name} - location: {engine.location}"
                for engine in engines
            ]
        )

        raise click.exceptions.UsageError(
            (
                f"Multiple Engines found for the provided name: {engine_name}\n"
                f"{extra_engines}\n"
                "run the command with the --location option to pick an engine"
            )
        )

    else:
        engine = engine_store.get_engine(engine_name, locations=location)

    engine_details = {
        "engine": {
            "name": engine.name,
            "description": engine.description,
            "location": engine.location,
            "engine_dir": engine.engine_dir,
            "digest": engine.digest,
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

            if engine_store.global_engine == name:
                engine_store.global_engine = None

    else:
        click.echo(f"[*] cleaning all engines from {engine_store.store_dir}")
        engine_store.clean_engines()
        engine_store.global_engine = None


@group.command(
    "install-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "-u",
    "--update",
    is_flag=True,
    help="Update the engine if it is installed",
)
@click.option(
    "-l",
    "--location",
    multiple=True,
    help="The location of the engine to install",
    default=["local", "remote", "hidden"],
)
@click.argument("name", required=False, type=click.STRING)
@exceptions.backend_handler()
@config.pass_options
def install_engine(opts, name, location, update):
    """
    Install an engine
    """

    engine_store.load_engines(locations=location, refresh=True)

    if name is None and opts.engine:
        name = opts.engine

    if name is None:
        raise click.exceptions.BadParameter(
            "Engine name missing - provide name with HAMLET_ENGINE or as an argument"
        )

    try:
        engine = engine_store.get_engine(name, locations=location)

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

    try:
        installed_engine = engine_store.get_engine(name, locations=["installed"])
    except EngineStoreMissingEngineException:
        installed_engine = False
        pass

    if installed_engine and update:
        engine.install()
        click.echo(f"[*] updating engine | {name} | digest: {engine.digest}")
    elif not installed_engine:
        engine.install()
        click.echo(f"[*] installing engine | {name} | digest: {engine.digest}")
    else:
        click.echo(f"[*] skipping engine update | {name} | digest: {engine.digest}")


@group.command(
    "set-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.argument("name", required=True, type=click.STRING)
@exceptions.backend_handler()
def set_engine(name):
    """
    Sets the global engine
    """
    engine = engine_store.get_engine(name, locations=["installed"])
    engine_store.global_engine = engine.name

    click.echo(f"[*] global engine set to {engine.name}")


@group.command(
    "get-engine", short_help="", context_settings=dict(max_content_width=240)
)
@exceptions.backend_handler()
@config.pass_options
def get_engine(opts):
    """
    Gets the current global engine
    """
    name = opts.engine if opts.engine else engine_store.global_engine
    click.echo(engine_store.get_engine(name, locations=["installed"]).name)


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

    engine_name = opts.engine if opts.engine else ENGINE_GLOBAL_NAME
    engine = engine_store.get_engine(engine_name, locations=["installed"])

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
