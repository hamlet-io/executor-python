import os
import subprocess
from hamlet import env as global_env
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
        [script_fullpath] + options_list + args
    )


def __env_params_to_envvars(env=None):
    cmd_env = {}
    for key, value in env.items():
        if value is not None:
            if isinstance(value, tuple):
                cmd_env[key.upper()] = ','.join(value)
            elif isinstance(value, bool):
                cmd_env[key.upper()] = str(bool).lower()
            else:
                cmd_env[key.upper()] = str(value)
    return cmd_env


def run(script_name, args, options, env, _is_cli):
    try:
        script_call_line = __cli_params_to_script_call(
            global_env.GENERATION_DIR,
            script_name,
            args=args,
            options=options
        )
        env_overrides = {**__env_params_to_envvars(env), **os.environ}
        process = subprocess.Popen(
            ['/bin/bash', '-c', script_call_line],
            stdout=None if _is_cli else subprocess.PIPE,
            stderr=None if _is_cli else subprocess.PIPE,
            encoding='utf-8',
            env=env_overrides
        )
        process.wait()
        if not _is_cli and process.returncode != 0:
            raise BackendException(process.stderr.read())
        if _is_cli and process.returncode != 0:
            raise BackendException(f'{script_name} failed to run')
    finally:
        try:
            process.kill()
        except ProcessLookupError:
            pass
