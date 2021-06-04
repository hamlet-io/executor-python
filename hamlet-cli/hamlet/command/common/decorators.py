import click
from click.types import StringParamType
import functools

from hamlet.command.common.config import Options


class CommaSplitParamType(StringParamType):
    envvar_list_splitter = ','

    def __repr__(self):
        return "STRING"


def common_cli_config_options(func):
    '''Add common CLI config options to commands'''

    @click.option(
        '-c',
        '--config-file',
        envvar='HAMLET_CONFIG_FILE',
        type=click.Path(dir_okay=True, exists=True, writable=False, resolve_path=True),
        help='The path to your config file',
    )
    @click.option(
        '-p',
        '--profile',
        default=None,
        envvar='HAMLET_PROFILE',
        help='The name of the profile to use for configuration',
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        '''
        Config file handling
        '''
        opts = ctx.ensure_object(Options)
        profile = kwargs.pop('profile')
        config_file = kwargs.pop('config_file')
        opts.load_config_file(path=config_file, profile=profile)
        kwargs['opts'] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_logging_options(func):
    '''Add commmon options for logging'''
    @click.option(
        '--log-level',
        envvar='GENERATION_LOG_LEVEL',
        type=click.Choice(
            ['fatal', 'error', 'warn', 'info', 'debug', 'trace'],
            case_sensitive=False
        ),
        default='info',
        help='The minimum log event level',
        show_default=True
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        '''
        Logging Options for the command line
        '''
        opts = ctx.ensure_object(Options)
        opts.log_level = kwargs.pop('log_level')
        kwargs['opts'] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_engine_options(func):
    '''Add common options for the engine'''

    @click.option(
        '--engine',
        envvar='HAMLET_ENGINE',
        help='The name of the engine to use',
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        '''
        Engine configuration options
        '''
        opts = ctx.ensure_object(Options)
        opts.engine = kwargs.pop('engine')
        kwargs['opts'] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_generation_options(func):
    '''Add commmon options for generation'''

    @click.option(
        '-p',
        '--generation-provider',
        envvar='GENERATION_PROVIDERS',
        help='plugins to load for output generation',
        default=['aws'],
        type=CommaSplitParamType(),
        multiple=True,
        show_default=True
    )
    @click.option(
        '-f',
        '--generation-framework',
        help='output framework to use for output generation',
        default='cf',
        show_default=True
    )
    @click.option(
        '-i',
        '--generation-input-source',
        help='source of input data to use when generating the output',
        default='composite',
        show_default=True
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        '''
        Logging Options for the command line
        '''
        opts = ctx.ensure_object(Options)
        opts.generation_provider = kwargs.pop('generation_provider')
        opts.generation_framework = kwargs.pop('generation_framework')
        opts.generation_input_source = kwargs.pop('generation_input_source')
        kwargs['opts'] = opts
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def common_district_options(func):
    '''Add Common options for district config'''

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
    @functools.wraps(func)
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
        return ctx.invoke(func, *args, **kwargs)

    return wrapper
