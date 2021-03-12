import functools
import click


class BackendException(Exception):
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg
