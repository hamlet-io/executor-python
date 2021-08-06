import click
import tempfile
import errno
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
                return object.__getattribute__(self, "_ctx").params[name]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{"show_default": True, **kwargs})

    def get_default(self, ctx):
        if callable(self.default):
            return self.default(self.ContextValuesGetter(ctx))
        return self.default

    @property
    def prompt(self):
        try:
            if not self.ctx.params.get("no_prompt"):
                if self.ctx.params.get("use_default") and self.default is not None:
                    return None
                if callable(self.__prompt) and not self.__prompt(
                    self.ContextValuesGetter(self.ctx)
                ):
                    return None
                return "[?] %s" % self.human_readable_name.replace("_", " ")
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
        return click.option(*args, **kwargs, cls=DynamicOption)(func)

    return decorator


def isWriteable(path):
    try:
        testfile = tempfile.TemporaryFile(dir=path)
        testfile.close()
    except (OSError, IOError) as e:
        if e.errno == errno.EACCES or e.errno == errno.EEXIST:
            return False
        e.filename = path
        raise
    return True


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
