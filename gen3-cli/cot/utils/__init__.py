import os


def cli_params_to_script_call(
    script_path,
    script_name,
    args=None,
    options=None
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
            else:
                options_list.append(str(key))
                options_list.append(str(value))
    script_fullpath=os.path.join(script_path, script_name)
    return ' '.join(
        [script_fullpath] +
        options_list +
        args
    )
