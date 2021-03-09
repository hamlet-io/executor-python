from hamlet.command import root as cli
from hamlet.command.common.exceptions import CommandError
from hamlet.backend import setup as setup_backend
from hamlet.backend.common.exceptions import BackendException


@cli.command(
    'setup',
    short_help='',
    context_settings=dict(
        max_content_width=240
    )
)
def setup(**kwargs):
    '''
    Sets up the local hamlet workspace
    '''
    try:
        setup_backend.run(**kwargs, _is_cli=True)

    except BackendException as e:
        raise CommandError(str(e))
