import os
import json
import subprocess


SHELL_SCRIPT_FILENAME = os.path.join(os.path.dirname(__file__), 'shell_vars_to_json.sh')


def shell_vars_to_json(filename=None, vars_mapping=None):
    args = [SHELL_SCRIPT_FILENAME, filename]
    for variable_name, variable_type in vars_mapping.items():
        args += [variable_name, variable_type]
    try:
        process = subprocess.Popen(
            ['bash', *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )
        process.wait()
        stderr = process.stderr.read()
        stdout = process.stdout.read()
        if stderr:
            raise RuntimeError(stderr)
        return json.loads(stdout)
    finally:
        try:
            process.kill()
        except ProcessLookupError:
            pass
