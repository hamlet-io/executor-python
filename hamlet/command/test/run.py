import os
import click
from hamlet.backend.test import run as test_run_backend
from hamlet.command.common.exceptions import CommandError


@click.command(
    "run",
    context_settings=dict(max_content_width=240),
    short_help="Run pytest on specified files",
)
@click.option(
    "-t",
    "--test",
    "tests",
    multiple=True,
    help="file or directory containing tests",
    type=click.Path(dir_okay=True, file_okay=True, exists=True),
)
@click.option(
    "-p", "--pytest-args", "pytest_args", help="additional arguments for pytest"
)
@click.option("-s", "--silent", "silent", is_flag=True, help="minimize pytest output")
def run(tests, pytest_args, silent):
    """
    Discover and run tests in specified files or/and directories. If no tests paths provided
    current directory used as tests discovery root.
    """
    if not tests:
        tests = (os.getcwd(),)

    try:
        test_run_backend.run(
            testpaths=tests,
            pytest_args=pytest_args,
            silent=silent,
        )
    except Exception as e:
        raise CommandError(str(e))
