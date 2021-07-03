from hamlet.command import root as cli
from hamlet.backend import setup as setup_backend
from hamlet.command.common import exceptions
from hamlet.command.common.config import pass_options


@cli.command("setup", short_help="", context_settings=dict(max_content_width=240))
@exceptions.backend_handler()
@pass_options
def setup(options, **kwargs):
    """
    Loads the plugins defined as part of the current district
    """
    args = {**options.opts, **kwargs}
    setup_backend.run(**args, _is_cli=True)
