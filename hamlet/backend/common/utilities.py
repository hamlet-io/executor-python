from typing import Any


def str_to_bool(value: Any) -> bool:
    """
    Return whether the provided string (or any value really) represents true. Otherwise false.
    Just like plugin server stringToBoolean.
    """
    if not value:
        return False
    return str(value).lower() in ("y", "yes", "t", "true", "on", "1")


def to_bool(value: Any, default) -> bool:
    """
    Converts string or None to bool
    """
    if isinstance(value, str):
        return str_to_bool(value)
    elif value is None:
        return default
    else:
        return value
