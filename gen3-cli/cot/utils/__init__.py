import os
import click


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


class DynamicCommand(click.Command):
    def invoke(self, ctx):
        if self.callback is not None:
            for param in self.params:
                try:
                    ctx.params[param.name]
                except KeyError:
                    if param.default is not None:
                        ctx.param[param.name] == param.default
        return super().invoke(ctx)


class DynamicOption(click.Option):

    class ContextValuesGetter:
        def __init__(self, ctx):
            self._ctx = ctx

        def __getattribute__(self, name):
            if name.startswith('_'):
                return object.__getattribute__(self, name)
            else:
                return object.__getattribute__(self, '_ctx').params[name]

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **{
                'show_default': True,
                **kwargs
            }
        )

    def get_default(self, ctx):
        if callable(self.default):
            return self.default(self.ContextValuesGetter(ctx))
        return self.default

    @property
    def prompt(self):
        try:
            if self.ctx.params.get('prompt'):
                if self.ctx.params.get('use_default') and self.default is not None:
                    return None
                if callable(self.__prompt) and not self.__prompt(self.ContextValuesGetter(self.ctx)):
                    return None
                return 'Enter %s' % self.human_readable_name.replace('_', ' ')
            else:
                return None
        except (AttributeError, KeyError):
            return self.__prompt

    @prompt.setter
    def prompt(self, value):
        self.__prompt = value

    def full_process_value(self, ctx, value):
        self.ctx = ctx
        return super().full_process_value(ctx, value)


def dynamic_option(*args, **kwargs):
    def decorator(func):
        return click.option(
            *args,
            **kwargs,
            cls=DynamicOption
        )(func)
    return decorator
