import os
import click
from cot.backend.test import run as test_run_backend


@click.command(
    'run',
    context_settings=dict(
        max_content_width=240
    )
)
@click.argument(
    'testpaths',
    nargs=-1
)
@click.option(
    '-s',
    '--silent',
    'silent',
    is_flag=True
)
def run(testpaths, silent):
    if not testpaths:
        testpaths.append(os.getcwd())
    test_run_backend.run(
        testpaths=testpaths,
        silent=silent
    )
