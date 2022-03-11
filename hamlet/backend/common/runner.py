import os
import subprocess
import shutil

from .exceptions import BackendException


def __cli_params_to_script_call(
    script_path, script_name, args=None, options=None, extra_script=None
):
    args = list(arg for arg in (args if args is not None else []) if arg is not None)
    options_list = []
    for key, value in options.items():
        if value is not None:
            if isinstance(value, bool):
                if value:
                    options_list.append(str(key))
            elif isinstance(value, tuple):
                for instance in value:
                    options_list.append(str(key))
                    options_list.append(str(f"'{instance}'"))
            else:
                options_list.append(str(key))
                options_list.append(str(f"'{value}'"))
    script_fullpath = os.path.join(script_path, script_name)
    if extra_script is not None:
        return " ".join([".", script_fullpath] + options_list + args + [extra_script])
    return " ".join([script_fullpath] + options_list + args)


def __env_params_to_envvars(env=None):
    cmd_env = {}
    for key, value in env.items():
        if value is not None:
            if isinstance(value, tuple):
                cmd_env[key.upper()] = ",".join(value)
            elif isinstance(value, bool):
                cmd_env[key.upper()] = str(value).lower()
            else:
                cmd_env[key.upper()] = str(value)
    return cmd_env


def run(
    script_name,
    args,
    options,
    env,
    engine,
    _is_cli,
    script_base_path_env="GENERATION_DIR",
    extra_script=None,
):
    env_overrides = {
        **os.environ,
        **__env_params_to_envvars(env),
    }

    if engine:
        env_overrides = {**env_overrides, **engine.environment}

    try:
        os.path.isdir(env_overrides[script_base_path_env])
    except TypeError:
        raise BackendException(
            f"Could not find script base path using env {script_base_path_env}: {env_overrides[script_base_path_env]}"
        )

    if shutil.which("bash") is None:
        raise BackendException("Could not find bash installation")

    try:
        script_call_line = __cli_params_to_script_call(
            env_overrides[script_base_path_env],
            script_name,
            args=args,
            options=options,
            extra_script=extra_script,
        )
        process = subprocess.Popen(
            [shutil.which("bash"), "-c", script_call_line],
            stdout=None if _is_cli else subprocess.PIPE,
            stderr=None if _is_cli else subprocess.PIPE,
            env=env_overrides,
            encoding="utf-8",
            bufsize=1,
        )

        stdout, stderr = process.communicate()
        if not _is_cli and process.returncode != 0:
            exception_message = "\n".join(
                [
                    f"script: {script_call_line}",
                    "",
                    "   stdout",
                    "".join((["#"] * 30)),
                    "",
                    stdout,
                    "   stderr",
                    "".join((["#"] * 30)),
                    "",
                    stderr,
                ]
            )
            raise BackendException(exception_message)
        if _is_cli and process.returncode != 0:
            raise BackendException(f"{script_name} failed to run")

    finally:
        try:
            process.kill()
        except ProcessLookupError:
            pass
        except UnboundLocalError:
            pass
