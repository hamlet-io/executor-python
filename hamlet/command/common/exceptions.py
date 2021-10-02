import functools
import click
from click._compat import get_text_stderr

import httpx._exceptions as httpx_exceptions
from click.exceptions import ClickException

from hamlet.backend.common.exceptions import BackendException
from hamlet.env import HAMLET_GLOBAL_CONFIG


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


class HamletHomeDirUnavailableException(CommandError):
    def show(self):
        click.secho(
            (
                f"[!] The hamlet home dir {HAMLET_GLOBAL_CONFIG.home_dir} is not assessible\n"
                f"[!] When testing access the reported error was:\n\n"
                f"  {self.message} \n\n"
                "[!] Check the permissions on the directory"
                " or change your home dir using the HAMLET_ENGINE_DIR environment variable\n"
            ),
            fg="red",
            bold=True,
            err=True,
        )

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
