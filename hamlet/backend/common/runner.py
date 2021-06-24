import os
import subprocess
import shutil

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

    env_overrides = {**global_env.ENGINE_ENV, **__env_params_to_envvars(env), **os.environ}
    try:
        os.path.isdir(env_overrides['GENERATION_DIR'])
    except TypeError:
        raise BackendException(
            f'Could not find hamlet bash script dir at GENERATION_DIR: {env_overrides["GENERATION_DIR"]}'
        )

    if shutil.which('bash') is None:
        raise BackendException('Could not find bash installation')

    try:
        script_call_line = __cli_params_to_script_call(
            env_overrides['GENERATION_DIR'],
            script_name,
            args=args,
            options=options
        )
        process = subprocess.Popen(
            [
                shutil.which('bash'),
                '-c',
                script_call_line
            ],
            stdout=None if _is_cli else subprocess.PIPE,
            stderr=None if _is_cli else subprocess.PIPE,
            env=env_overrides,
            encoding='utf-8',
            bufsize=1,
        )

        stdout, stderr = process.communicate()
        if not _is_cli and process.returncode != 0:
            exception_message = '\n'.join(
                [
                    f'script: {script_call_line}',
                    '',
                    ''.join((['#'] * 50)),
                    '   stdout',
                    ''.join((['#'] * 50)),
                    '',
                    stdout,
                    ''.join((['#'] * 50)),
                    '   stderr',
                    ''.join((['#'] * 50)),
                    '',
                    stderr,
                ]
            )
            raise BackendException(exception_message)
        if _is_cli and process.returncode != 0:
            raise BackendException(f'{script_name} failed to run')

    finally:
        try:
            process.kill()
        except ProcessLookupError:
            pass
        except UnboundLocalError:
            pass
