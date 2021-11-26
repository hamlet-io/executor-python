import click
import os

from click_configfile import Param


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
            if name.startswith("_"):
                return object.__getattribute__(self, name)
            else:
                return object.__getattribute__(self, "_ctx").params.get(name, None)

    def get_default(self, ctx, call=True):
        value = ctx.lookup_default(self.name, call=False)

        if value is None:
            if callable(self.default):
                value = self.default(self.ContextValuesGetter(ctx))
            else:
                value = self.default

        if call and callable(value):
            return value()

        return value


def dynamic_option(*args, **kwargs):
    def decorator(func):
        return click.option(*args, **kwargs, cls=DynamicOption)(func)

    return decorator


class ConfigParam(Param):
    # For compatibility with click>=7.0
    def __init__(self, *args, **kwargs):
        super(ConfigParam, self).__init__(*args, **kwargs)
        self.ctx = None

    def parse(self, text):
        if text:
            text = text.strip()
        if self.type.name == "boolean":
            if not text:
                return None
        return super(ConfigParam, self).parse(text)

    def get_error_hint(self, ctx):
        if self.ctx:
            files = []
            for path in self.ctx.config_searchpath:
                for filename in self.ctx.config_files:
                    files.append(os.path.join(path, filename))
            files = " or ".join(files)
            msg = f"{self.name} in {files}"
        else:
            msg = f"{self.name} in a config file"
        return msg
