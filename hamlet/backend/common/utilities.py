from distutils.util import strtobool


def to_bool(value, default):
    """
    Converts string or None to bool
    """
    if isinstance(value, str):
        return strtobool(value)
    elif value is None:
        return default
    else:
        return value
