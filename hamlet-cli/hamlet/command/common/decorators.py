import click
import functools

from hamlet.command.common.config import Options


def common_cli_config_options(f):
    """Add common CLI config options to commands."""

    @click.option(
        "-c",
        "--config-file",
        envvar="HAMLET_CONFIG_FILE",
        type=click.Path(dir_okay=True, exists=True, writable=False, resolve_path=True),
        help="The path to your config file.",
    )
    @click.option(
        "-p",
        "--profile",
        default=None,
        envvar="HAMLET_PROFILE",
        help="The name of the profile to use for configuration.",
    )
    @click.pass_context
    @functools.wraps(f)
    def wrapper(ctx, *args, **kwargs):
        '''
        Config file handling
        '''
        opts = ctx.ensure_object(Options)
        profile = kwargs.pop("profile")
        config_file = kwargs.pop("config_file")
        opts.load_config_file(path=config_file, profile=profile)
        kwargs["opts"] = opts
        return ctx.invoke(f, *args, **kwargs)

    return wrapper


def common_district_options(f):
    """Common options for district config"""

    @click.option(
        "--root-dir",
        envvar="ROOT_DIR",
        help="The root CMDB directory (default: CMDB current location)",
    )
    @click.option(
        "--tenant",
        envvar="TENANT",
        help="The tenant name to use (default: CMDB current location)",
    )
    @click.option(
        "--account",
        envvar="ACCOUNT",
        help="The account name to use",
    )
    @click.option(
        "--product",
        envvar="PRODUCT",
        help="The product name to use (default: CMDB current location)",
    )
    @click.option(
        "--environment",
        envvar="ENVIRONMENT",
        help="The environment name to use (default: CMDB current location)",
    )
    @click.option(
        "--segment",
        envvar="SEGMENT",
        help="The segment name to use (default: CMDB current location)"
    )
    @click.pass_context
    @functools.wraps(f)
    def wrapper(ctx, *args, **kwargs):
        '''
        District options from cmd line or file
        '''
        opts = ctx.ensure_object(Options)
        opts.root_dir = kwargs.pop("root_dir")
        opts.tenant = kwargs.pop("tenant")
        opts.account = kwargs.pop("account")
        opts.product = kwargs.pop("product")
        opts.environment = kwargs.pop("environment")
        opts.segment = kwargs.pop("segment")
        kwargs["opts"] = opts
        return ctx.invoke(f, *args, **kwargs)

    return wrapper
