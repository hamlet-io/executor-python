import click


def validate_entrance_inputs(ctx, param, value):
    """
    Custom validation for entrance inputs which are provided as Key=Value
    strings
    """
    try:
        value = dict([arg.split("=", 1) for arg in value])
    except ValueError:
        raise click.BadParameter("input arguments must be in 'Key=Value' format")

    return value
