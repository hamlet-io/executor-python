import os.path


__all__ = [
    "__title__",
    "__summary__",
    "__url__",
    "__repository_url__",
    "__author__",
    "__email__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None

__title__ = "hamlet"
__summary__ = "Building your infrastructure"
__url__ = "https://hamlet.io"
__repository_url__ = "https://github.com/hamlet-io/executor-python"

__author__ = "Hamlet"
__email__ = "help@hamlet.io"
