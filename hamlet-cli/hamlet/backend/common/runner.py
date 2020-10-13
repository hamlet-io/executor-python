import os
import subprocess
from hamlet import env
from .exceptions import BackendException


def __cli_params_to_script_call(
    script_path,
    script_name,
    args=None,
    options=None,

):
    args = list(
        arg
        for arg in (args if args is not None else [])
        if arg is not None
    )
    options_list = []
    for key, value in options.items():
        if value is not None:
            if isinstance(value, bool):
                if value:
                    options_list.append(str(key))
            elif isinstance(value, tuple):
                for instance in value:
                    options_list.append(str(key))
                    options_list.append(str(instance))
            else:
                options_list.append(str(key))
                options_list.append(str(value))
    script_fullpath = os.path.join(script_path, script_name)
    return ' '.join(
        [script_fullpath] +
        options_list +
        args
    )


def run(script_name, args, options, _is_cli):
    try:
        script_call_line = __cli_params_to_script_call(
            env.GENERATION_DIR,
            script_name,
            args=args,
            options=options
        )
        process = subprocess.Popen(
            ['/bin/bash', '-c', script_call_line],
            stdout=None if _is_cli else subprocess.PIPE,
            stderr=None if _is_cli else subprocess.PIPE,
            encoding='utf-8'
        )
        process.wait()
        if not _is_cli and process.returncode != 0:
            raise BackendException(process.stderr.read())
    finally:
        try:
            process.kill()
        except ProcessLookupError:
            pass
