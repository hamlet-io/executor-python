import functools
import click


class BackendException(Exception):
    pass


class UserFriendlyBackendException(BackendException):
    pass


def handler():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except UserFriendlyBackendException as e:
                click.echo(str(e))
            except BackendException as e:
                click.echo(str(e), err=True)
