import subprocess
from cot import utils
from cot import env


def run(
    reference_type=None,
    reference_output_dir=None
):
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
