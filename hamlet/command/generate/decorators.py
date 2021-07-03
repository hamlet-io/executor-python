import click
import functools
import os


def common_generate_options(f):
    """Add common options for the generate command group"""

    @functools.wraps(f)
    @click.option(
        "--use-default",
        help="If a default value is set, skip prompt for the value",
        is_flag=True,
    )
    @click.option(
        "--no-prompt",
        help="Disable prompting for missing inputs and error on missing values",
        is_flag=True,
    )
    @click.option(
        "--output-dir",
        "-o",
        help="The directory to save the generated content",
        show_default=True,
        type=click.Path(file_okay=False, dir_okay=True, writable=True),
        default=os.getcwd(),
    )
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)

    return wrapper
