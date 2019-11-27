import os
import click
from tabulate import tabulate


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
    script_fullpath = os.path.join(script_path, script_name)
    return ' '.join(
        [script_fullpath] +
        options_list +
        args
    )


def click_prompt_missing_option(
    kwargs,
    key,
    *prompt_args,
    use_default=False,
    **prompt_kwargs
):
    value = kwargs.get(key)
    try:
        text, *prompt_args = prompt_args
    except ValueError:
        text = None
    text = (text or prompt_kwargs.get('text')) or "Enter %s" % key.replace('_', ' ')
    prompt_kwargs['text'] = text

    default = prompt_kwargs.get('default')
    if value is None:
        if use_default and default is not None:
            kwargs[key] = default
        else:
            kwargs[key] = click.prompt(*prompt_args, **prompt_kwargs)


def click_kwargs_confirmation_prompt(
    kwargs,
    *confirm_args,
    **confirm_kwargs
):
    try:
        text, *confirm_args = confirm_args
    except ValueError:
        text = None
    text = (text or confirm_kwargs.get('text')) or 'Is everything correct?'
    confirm_kwargs['text'] = text
    lines = []
    i = 1
    for key, value in kwargs.items():
        name = key.replace('_', ' ')
        lines.append([i, name, value])
        i += 1
    click.echo(
        tabulate(
            lines,
            ['№', 'parameter', 'value'],
            tablefmt='psql'
        )
    )
    return click.confirm(*confirm_args, **confirm_kwargs)


class ClickMissingOptionsPrompt():
    def __init__(self, ctx, kwargs, use_default):
        self.__ctx = ctx
        self.__kwargs = kwargs
        self.__use_default = use_default

    def __prompt_missing_option(
        self,
        key,
        **prompt_kwargs
    ):
        value = self.__kwargs.get(key)
        prompt_kwargs['text'] = prompt_kwargs.get('text') or "Enter %s" % key.replace('_', ' ')
        prompt_kwargs['type'] = prompt_kwargs.get('type') or self.__get_option_type(key)
        default = prompt_kwargs.get('default')
        if value is None:

            if self.__use_default and default is not None:
                value = default
            else:
                value = click.prompt(**prompt_kwargs)
            self.__kwargs[key] = value
            return value

    def __get_option_type(self, name):
        for param in self.__ctx.command.params:
            if param.name == name:
                return param.type
        return None

    def confirm(
        self,
        **confirm_kwargs
    ):
        confirm_kwargs['text'] = confirm_kwargs.get('text') or 'Is everything correct?'
        lines = []
        i = 1
        for key, value in self.__kwargs.items():
            if value is None:
                continue
            name = key.replace('_', ' ')
            lines.append([i, name, value])
            i += 1
        click.echo(
            tabulate(
                lines,
                ['№', 'parameter', 'value'],
                tablefmt='psql'
            )
        )
        return click.confirm(**confirm_kwargs)

    def __getattribute__(self, name):
        if name.startswith('_') or name == 'confirm':
            return object.__getattribute__(self, name)
        else:
            def prompt(*args, **kwargs):
                return self.__prompt_missing_option(
                    name,
                    *args,
                    **kwargs
                )
            return prompt
