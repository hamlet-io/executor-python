from hamlet.command import root as cli
from hamlet.command.common.exceptions import CommandError
from hamlet.backend import setup as setup_backend
from hamlet.backend.common.exceptions import BackendException
from hamlet.command.common.config import pass_options

@cli.command(
    'setup',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
@pass_options
def setup(options, **kwargs):
    '''
    Sets up the local hamlet workspace
    '''
    args = {
        **options.opts,
        **kwargs
    }
    try:
        setup_backend.run(**args, _is_cli=True)

    except BackendException as e:
        raise CommandError(str(e))
