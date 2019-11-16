import subprocess
import click
from cot import utils
from cot import env


@click.command(
    'reference',
    short_help='Create a Codeontap Component Reference',
    context_settings=dict(
        max_content_width=240
    )
)
@click.option(
    '-t',
    '--reference-type',
    required=True,
    help='type of object you need the reference for'
)
@click.option(
    '-o',
    '--reference-output-dir',
    help='output directory',
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True
    )
)
def reference(
    reference_type,
    reference_output_dir
):
    """
    Create a Codeontap Component Reference
    """
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'createReference.sh',
        options={
            '-t': reference_type,
            '-o': reference_output_dir
        }
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
