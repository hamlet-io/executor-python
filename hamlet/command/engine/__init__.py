import json
import os

import click
from tabulate import tabulate

from hamlet.backend.engine.engine_code_source import EngineCodeSourceBuildData
from hamlet.backend.engine.exceptions import (
    EngineStoreMissingEngineException,
    HamletEngineInvalidVersion,
)
from hamlet.command import root as cli
from hamlet.command.common import config, exceptions
from hamlet.command.common.display import json_or_table_option, wrap_text


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
@config.pass_options
def list_engine_locations(options):
    """
    Lists the engine locations
    """
    data = []
    for k, location in options.engine_store.engine_locations.items():
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
@config.pass_options
def list_engines(options, location):
    """
    Lists the engines available
    """
    options.engine_store.load_engines(locations=location, refresh=True)
    data = []
    for engine_instance in options.engine_store.get_engines(locations=location):
        data.append(
            {
                "name": engine_instance.name,
                "location": engine_instance.location,
                "description": engine_instance.description,
                "short_digest": engine_instance.short_digest,
                "digest": engine_instance.digest,
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
def describe_engine(options, name, location):
    """
    Provides a detailed description of an engine
    """

    location = None if not location else [location]

    if name:
        options.engine_store.load_engines(locations=location, refresh=True)
        engines = [
            x
            for x in options.engine_store.get_engines(locations=location)
            if x.name == name
        ]
        if len(engines) > 1:
            extra_engines = "\n".join(
                [f" - name: {x.name} - location: {x.location}" for x in engines]
            )

            raise click.exceptions.UsageError(
                (
                    f"Multiple Engines found for the provided name: {name}\n"
                    f"{extra_engines}\n"
                    "run the command with the --location option to pick an engine"
                )
            )
        else:
            engine_instance = engines[0]

    else:
        engine_instance = options.engine

    engine_details = {
        "engine": {
            "name": engine_instance.name,
            "description": engine_instance.description,
            "location": engine_instance.location,
            "engine_dir": engine_instance.engine_dir,
            "digest": engine_instance.digest,
        },
        "environment": engine_instance.environment,
        "install_state": engine_instance.install_state,
    }

    sources = []
    for source in engine_instance.sources:
        try:
            source_digest = source.digest
        except BaseException as e:
            click.secho(
                f"[!] Source check failed {engine_instance.name} - {source.name}",
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
    for part in engine_instance.parts:
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
@config.pass_options
def clean_engines(options, name):
    """
    Clean local engine store
    """
    if name:
        for x in name:
            click.echo(f"[*] cleaning {x} from {options.engine_store.store_dir}")
            options.engine_store.clean_engine(x)

            if options.engine_store.default_engine == name:
                options.engine_store.default_engine = None

    else:
        click.echo(f"[*] cleaning all engines from {options.engine_store.store_dir}")
        options.engine_store.clean_engines()
        options.engine_store.default_engine = None


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
def install_engine(options, name, location, update):
    """
    Install an engine
    """

    options.engine_store.load_engines(locations=location, refresh=True)

    if name is None and options.engine:
        name = options.engine.name

    if name is None:
        raise click.exceptions.BadParameter(
            "Engine name missing - provide name with HAMLET_ENGINE or as an argument"
        )

    try:
        engine_instance = options.engine_store.get_engine(name, locations=location)

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
        installed_engine = options.engine_store.get_engine(
            name, locations=["installed"]
        )
    except EngineStoreMissingEngineException:
        installed_engine = False
        pass

    if installed_engine and update:
        engine_instance.install()
        click.echo(f"[*] updating engine | {name} | digest: {engine_instance.digest}")
    elif not installed_engine:
        engine_instance.install()
        click.echo(f"[*] installing engine | {name} | digest: {engine_instance.digest}")
    else:
        click.echo(
            f"[*] skipping engine update | {name} | digest: {engine_instance.digest}"
        )


@group.command(
    "set-engine", short_help="", context_settings=dict(max_content_width=240)
)
@click.argument("name", required=True, type=click.STRING)
@exceptions.backend_handler()
@config.pass_options
def set_engine(options, name):
    """
    Sets the default engine
    """
    engine = options.engine_store.get_engine(name, locations=["installed"])
    options.engine_store.default_engine = engine.name

    click.echo(f"[*] default engine set to {engine.name}")


@group.command(
    "get-engine", short_help="", context_settings=dict(max_content_width=240)
)
@exceptions.backend_handler()
@config.pass_options
def get_engine(options):
    """
    Gets the current global engine
    """
    name = (
        options.engine.name if options.engine else options.engine_store.default_engine
    )
    click.echo(options.engine_store.get_engine(name, locations=["installed"]).name)


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
