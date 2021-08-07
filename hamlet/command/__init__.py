import click
import os

from hamlet.command.common import decorators
from hamlet.command.common.exceptions import backend_handler
from hamlet.backend.engine.exceptions import HamletEngineInvalidVersion

from hamlet.utils import isWriteable
from hamlet.env import HAMLET_GLOBAL_CONFIG
from hamlet.command.common.engine_setup import (
    check_engine_update,
    setup_global_engine,
    get_engine_env,
)

try:
    from hamlet.__version__ import version
except ImportError:
    version = "unknown"


@click.group("root", context_settings=dict(max_content_width=240))
@click.version_option(version)
@decorators.common_cli_config_options
@decorators.common_generation_options
@decorators.common_logging_options
@decorators.common_engine_options
@decorators.common_district_options
@click.pass_context
@backend_handler()
def root(ctx, opts):
    """
    hamlet deploy
    """

    try:
        os.makedirs(HAMLET_GLOBAL_CONFIG.home_dir, exist_ok=True)
    except OSError:
        pass

    homeWritable = isWriteable(HAMLET_GLOBAL_CONFIG.home_dir)

    if not homeWritable:
        click.secho(
            (
                f"[!] The hamlet home dir {HAMLET_GLOBAL_CONFIG.home_dir} isn't writable by this user\n"
                "[!] Check the permissions on the directory"
                " or change your home dir using the HAMLET_ENGINE_DIR environment variable\n"
                "[!] We will continue but some parts of hamlet won't work and will raise errors of their own"
            ),
            fg="red",
            bold=True,
            err=True,
        )

    if homeWritable:
        try:
            setup_global_engine(opts.engine)

        except HamletEngineInvalidVersion:
            pass

        if ctx.invoked_subcommand != "engine":

            check_engine_update(
                opts.engine, opts.engine_update_install, opts.engine_update_interval
            )

        get_engine_env(opts.engine)
