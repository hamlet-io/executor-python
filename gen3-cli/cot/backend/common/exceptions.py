import functools
import click


class BackendException(Exception):
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg


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
        return wrapper
    return decorator
