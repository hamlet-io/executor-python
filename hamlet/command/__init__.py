import click
import os
import tempfile

from hamlet.command.common import decorators
from hamlet.command.common.exceptions import (
    backend_handler,
    HamletHomeDirUnavailableException,
)
from hamlet.env import HAMLET_GLOBAL_CONFIG
from hamlet.command.common.engine_setup import (
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
        testfile = tempfile.TemporaryFile(dir=HAMLET_GLOBAL_CONFIG.home_dir)
        testfile.close()

    except OSError as e:
        raise HamletHomeDirUnavailableException(str(e))

    setup_global_engine(opts.engine)
    get_engine_env(opts.engine)
