import click
import os

from hamlet import __about__

from hamlet.command.common import decorators
from hamlet.command.common.exceptions import backend_handler

from hamlet.utils import isWriteable
from hamlet.env import HAMLET_HOME_DIR
from hamlet.command.common.engine_setup import (
    setup_initial_engines,
    update_engine
)


@click.group('root')
@click.version_option(__about__.__version__)
@decorators.common_engine_options
@decorators.common_district_options
@decorators.common_cli_config_options
@decorators.common_generation_options
@decorators.common_logging_options
@click.pass_context
@backend_handler()
def root(ctx, opts):
    '''
    hamlet deploy
    '''

    try:
        os.makedirs(HAMLET_HOME_DIR, exist_ok=True)
    except OSError:
        pass

    if not isWriteable(HAMLET_HOME_DIR):
        click.echo(
            click.style(
                (
                    f"[!] The hamlet home dir {HAMLET_HOME_DIR} isn't writable by this user\n"
                    "[!] Check the permissions on the directory"
                    " or change your home dir using the HAMLET_ENGINE_DIR environment variable\n"
                    "[!] We will continue but some parts of hamlet won't work and will raise errors of their own"
                ),
                fg='red',
                bold=True
            ),
            err=True
        )

    if isWriteable(HAMLET_HOME_DIR):
        setup_initial_engines(opts.engine)
        update_engine(opts.engine, opts.auto_update_engine)
