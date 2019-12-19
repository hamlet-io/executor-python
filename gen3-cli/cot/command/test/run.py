import os
import click
from cot.backend.test import test_run_backend


@click.command(
    'run',
    context_settings=dict(
        max_content_width=240
    )
)
@click.argument(
    'tests',
    nargs=-1
)
def run(tests):
    if not tests:
        tests.append(os.getcwd())
    test_run_backend.run(*tests)
