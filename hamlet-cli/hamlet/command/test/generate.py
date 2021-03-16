import os
import click
from hamlet.backend.test.generate import run as test_generate_backend
from hamlet.command.common import exceptions


@click.command(
    'generate',
    context_settings=dict(
        max_content_width=240
    ),
    short_help='Generate tests based on .tescase.json files'
)
@click.option(
    '-f',
    '--filename',
    'filenames',
    multiple=True,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        exists=True
    ),
    help='path to testcase file'
)
@click.option(
    '-d',
    '--directory',
    'directory',
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=True
    ),
    default='.',
    show_default=True,
    help='directory to scan for testcase files[depth=1]',
)
@click.option(
    '-o',
    '--output',
    'output',
    type=click.Path(
        file_okay=True,
        dir_okay=False
    ),
    help='output file path'
)
@exceptions.backend_handler()
def geneate(
    filenames,
    output,
    directory
):
    """
    Used to generate pytests from testcase files.

    \b
    Test type determined by target file extension:

    \b
        1. ".json" - cf template test

    \b
    Note:
    \b
        1. When no files and no directory provided current directory is used to scan for testcase files(depth=1).
        2. Multiple testcase files merged in runtime therefore all testcases must have unique names.
        3. When no output file path provided output will be sent to stdout
        4. Tescase files must have ".testcase.json" extension. Otherwise command will complain and not run.

    \b
    Testcase file structure:

    \b
    {
        "casename":{
            "filename": "/path/to/subject.json",
            "no_lint":True,
            "no_vulnerability_check":True,
            "structure": {
                "exists":[
                    "path.in.json.obj",
                    "path.in.json.array[0].test"
                ],
                "match":[
                    [
                        "path.to.json.object",
                        {
                            "key": "value"
                        }
                    ],
                    [
                        "path.to.json.scalar",
                        "scalar value"
                    ],
                    [
                        "path.to.json.value.in.array[10]",
                        -5
                    ]
                ],
                "resource":[
                    [
                        "resourceName",
                        "resourceType"
                    ]
                ],
                "output":[
                    "outputName"
                ],
                "not_empty":[
                    "not.empty.path"
                ],
                "length":[
                    "path.to.json.array",
                    10
                ]
            }
        }
    }

    """
    directory = os.path.abspath(directory) if directory == '.' else directory
    result = test_generate_backend(
        filenames=filenames,
        output=output,
        directory=directory
    )
    if not output:
        click.echo(result)
