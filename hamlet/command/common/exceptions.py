import functools
import click
from click._compat import get_text_stderr

import httpx._exceptions as httpx_exceptions
from click.exceptions import ClickException

from hamlet.backend.common.exceptions import BackendException


class CommandError(ClickException):
    """An exception occurred during processing"""

    def show(self, file=None):
        if file is None:
            file = get_text_stderr()
        click.echo(
            click.style("[!] Error Running Command", fg="red", bold=True), err=True
        )
        click.echo("")
        click.echo(self.format_message(), file=file, err=True)

    def format_message(self):
        return click.style(str(self.message))


def backend_handler():
    """Handles backend errors with a formatted click exception message"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except httpx_exceptions.RequestError as e:

                msg = f"HTTP error | url: {e.request.url} | msg: {str(e)}"
                raise CommandError(msg)

            except BackendException as e:

                raise CommandError(str(e))

        return wrapper

    return decorator
