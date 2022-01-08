import subprocess
import shutil


def run(Command=None, env={}):
    """
    Run a bash command and use the stdout as the returned result
    """
    command_result = subprocess.check_output(
        [shutil.which("bash"), "-c", Command],
        text=True,
    )

    return {"Properties": {"result": command_result.rstrip("\n")}}
