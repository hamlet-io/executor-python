import os
import click
from click.types import StringParamType
import functools

from hamlet.command.common.config import Options


def get_home_dir_default(subdir=""):
    return os.path.join(
        click.get_app_dir(app_name="hamlet", force_posix=True, roaming=False), subdir
    )


class CommaSplitParamType(StringParamType):
    envvar_list_splitter = ","

    def __repr__(self):
        return "STRING"


def common_cli_config_options(func):
    """Add common CLI config options to commands"""

    @click.option(
        "-p",
        "--profile",
        default=None,
        envvar="HAMLET_PROFILE",
        help="The name of the profile to use for configuration",
        show_envvar=True,
    )
    @click.option(
        "--cli-config-dir",
        type=click.Path(file_okay=False, dir_okay=True, readable=True),
        envvar="HAMLET_CLI_CONFIG_DIR",
        default=get_home_dir_default("config"),
        help="The directory where profile configuration is stored",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--hamlet-home-dir",
        type=click.Path(file_okay=False, dir_okay=True, readable=True, writable=True),
        envvar="HAMLET_HOME_DIR",
        default=get_home_dir_default(),
        help="The home directory used by hamlet",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--cli-cache-dir",
        type=click.Path(file_okay=False, dir_okay=True, readable=True, writable=True),
        envvar="HAMLET_CLI_CACHE_DIR",
        default=get_home_dir_default("cache"),
        help="The directory where the cli can cache generation outputs",
        show_default=True,
        show_envvar=True,
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        """
        Config file handling
        """
        opts = ctx.ensure_object(Options)
        opts.cli_cache_dir = kwargs.pop("cli_cache_dir")
        opts.hamlet_home_dir = kwargs.pop("hamlet_home_dir")
        opts.load_config_file(
            profile=kwargs.pop("profile"), searchpath=kwargs.pop("cli_config_dir")
        )

        kwargs["opts"] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_logging_options(func):
    """Add commmon options for logging"""

    @click.option(
        "--log-level",
        envvar="GENERATION_LOG_LEVEL",
        type=click.Choice(
            ["fatal", "error", "warn", "info", "debug", "trace"], case_sensitive=False
        ),
        default="info",
        help="The minimum log event level",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--log-format",
        envvar="GENERATION_LOG_FORMAT",
        type=click.Choice(["compact", "full"], case_sensitive=False),
        default="compact",
        help="The format used for engine log messages",
        show_default=True,
        show_envvar=True,
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        """
        Logging Options for the command line
        """
        opts = ctx.ensure_object(Options)
        opts.log_level = kwargs.pop("log_level")
        opts.log_format = kwargs.pop("log_format")

        kwargs["opts"] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_engine_options(func):
    """Add common options for the engine"""

    @click.option(
        "--engine",
        envvar="HAMLET_ENGINE",
        help="The name of the engine to use",
        show_envvar=True,
    )
    @click.option(
        "--engine-dir",
        type=click.Path(
            dir_okay=True,
            file_okay=False,
            writable=True,
            readable=True,
        ),
        default=get_home_dir_default("engine"),
        envvar="HAMLET_ENGINE_DIR",
        help="The location of the hamlet engine store",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--engine-config-dir",
        type=click.Path(
            dir_okay=True,
            file_okay=False,
            writable=True,
            readable=True,
        ),
        default=get_home_dir_default("config"),
        envvar="HAMLET_ENGINE_CONFIG",
        help="The location of the hamlet engine config file for local engines",
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "--engine-search-locations",
        multiple=True,
        default=["installed", "local", "remote"],
        type=click.Choice(["installed", "local", "remote", "hidden"]),
        show_default=True,
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        """
        Engine configuration options
        """
        opts = ctx.ensure_object(Options)
        opts.set_engine_store(
            kwargs.pop("engine_dir"), [kwargs.pop("engine_config_dir")]
        )
        opts.set_engine(kwargs.pop("engine"), kwargs.pop("engine_search_locations"))
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_generation_options(func):
    """Add commmon options for generation"""

    @click.option(
        "-p",
        "--generation-provider",
        envvar="GENERATION_PROVIDERS",
        help="plugins to load for output generation",
        default=["aws"],
        type=CommaSplitParamType(),
        multiple=True,
        show_default=True,
        show_envvar=True,
    )
    @click.option(
        "-f",
        "--generation-framework",
        help="output framework to use for output generation",
        default="cf",
        show_default=True,
    )
    @click.option(
        "-i",
        "--generation-input-source",
        help="source of input data to use when generating the output",
        default="composite",
        show_default=True,
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        """
        Logging Options for the command line
        """
        opts = ctx.ensure_object(Options)
        opts.generation_provider = kwargs.pop("generation_provider")
        opts.generation_framework = kwargs.pop("generation_framework")
        opts.generation_input_source = kwargs.pop("generation_input_source")

        kwargs["opts"] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_district_options(func):
    """Add Common options for district config"""

    @click.option(
        "--root-dir",
        envvar="ROOT_DIR",
        help="The root CMDB directory (default: CMDB current location)",
        show_envvar=True,
    )
    @click.option(
        "--district-type",
        envvar="DISTRICT_TYPE",
        help="The type of district to target",
        default="segment",
        show_envvar=True,
    )
    @click.option(
        "--tenant",
        envvar="TENANT",
        help="The tenant name to use (default: CMDB current location)",
        show_envvar=True,
    )
    @click.option(
        "--account",
        envvar="ACCOUNT",
        help="The account name to use",
        show_envvar=True,
    )
    @click.option(
        "--product",
        envvar="PRODUCT",
        help="The product name to use (default: CMDB current location)",
        show_envvar=True,
    )
    @click.option(
        "--environment",
        envvar="ENVIRONMENT",
        help="The environment name to use (default: CMDB current location)",
        show_envvar=True,
    )
    @click.option(
        "--segment",
        envvar="SEGMENT",
        help="The segment name to use (default: CMDB current location)",
        show_envvar=True,
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        """
        District options from cmd line or file
        """
        opts = ctx.ensure_object(Options)
        opts.root_dir = kwargs.pop("root_dir")
        opts.district_type = kwargs.pop("district_type")
        opts.tenant = kwargs.pop("tenant")
        opts.account = kwargs.pop("account")
        opts.product = kwargs.pop("product")
        opts.environment = kwargs.pop("environment")
        opts.segment = kwargs.pop("segment")

        kwargs["opts"] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper
