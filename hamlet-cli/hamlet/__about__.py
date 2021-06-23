import os.path


__all__ = [
    '__title__',
    '__summary__',
    '__uri__',
    '__version__',
    '__commit__',
    '__author__',
    '__email__',
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None

__title__ = 'hamlet-cli'
__summary__ = 'Building your infrastructure'
__url__ = "https://hamlet.io"

__version__= '8.2.0-dev16'

if base_dir is not None and os.path.exists(os.path.join(base_dir, ".commit")):
    with open(os.path.join(base_dir, ".commit")) as fp:
        __commit__ = fp.read().strip()
else:
    __commit__ = None

__author__ = 'Hamlet'
__email__ = 'help@hamlet.io'
