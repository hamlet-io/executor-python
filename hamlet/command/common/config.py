import click
import os

from click_configfile import ConfigFileReader, SectionSchema, matches_section
from hamlet.env import HAMLET_GLOBAL_CONFIG
from hamlet.utils import ConfigParam


class ConfigSchema(object):
    """Schema for standard configuration."""

    @matches_section("profile:*")
    class Profile(SectionSchema):
        """Profile-specific configuration schema."""

        #: the root directory of the CMDB
        root_dir = ConfigParam(name="root_dir", type=click.Path())

        #: the name of the tenant
        tenant = ConfigParam(name="tenant", type=str)

        #: the name of the account
        account = ConfigParam(name="account", type=str)

        #: the name of the product
        product = ConfigParam(name="product", type=str)

        #: the name of the environment
        environment = ConfigParam(name="environment", type=str)

        #: the name of the segment
        segment = ConfigParam(name="segment", type=str)

        #: the name of the engine to use within this profile
        engine = ConfigParam(name="engine", type=str)


class ConfigReader(ConfigFileReader):
    """Reader for standard configuration."""

    config_files = ["config.ini", "config"]
    config_name = "standard"
    config_searchpath = []
    config_section_schemas = [ConfigSchema.Profile]

    @classmethod
    def select_config_schema_for(cls, section_name):
        section_schema = super(ConfigReader, cls).select_config_schema_for(section_name)
        for v in section_schema.__dict__:
            if isinstance(v, ConfigParam):
                v.ctx = cls
        return section_schema

    @classmethod
    def load_config(cls, opts, profile=None):
        """Load a configuration file into an options object."""

        if os.path.exists(HAMLET_GLOBAL_CONFIG.config_dir):
            if os.path.isdir(HAMLET_GLOBAL_CONFIG.config_dir):
                cls.config_searchpath.insert(0, HAMLET_GLOBAL_CONFIG.config_dir)

        config = cls.read_config()
        values = config.get("default", {})
        cls._load_values_into_opts(opts, values)

        if profile and profile != "default":
            values = config.get(f"profile:{profile}", {})
            cls._load_values_into_opts(opts, values)

        return values

    @staticmethod
    def _load_values_into_opts(opts, values):
        for k, v in values.items():
            if v is None:
                continue
            if isinstance(v, str):
                if v.startswith('"') or v.startswith("'"):
                    v = v[1:]
                if v.endswith('"') or v.endswith("'"):
                    v = v[:-1]
                if not v:
                    continue
            else:
                if v is None:
                    continue
            setattr(opts, k, v)


class Options:
    """Options object that holds config for the application."""

    def __init__(self, *args, **kwargs):
        """Initialise a new Options object."""
        super(Options, self).__init__(*args, **kwargs)
        self.opts = {}
        for k, v in kwargs:
            setattr(self, k, v)

    @staticmethod
    def get_config_reader():
        """Get the config reader class."""
        return ConfigReader

    def load_config_file(self, profile=None):
        """Load the config file."""
        config_cls = self.get_config_reader()
        return config_cls.load_config(self, profile=profile)

    @property
    def cli_config_dir(self):
        """The cli config dir"""
        return self._get_option("cli_config_dir")

    @cli_config_dir.setter
    def cli_config_dir(self, value):
        """Set the cli config dir"""
        self._set_option("cli_config_dir", value)

    @property
    def log_level(self):
        """Get the log_level setting"""
        return self._get_option("log_level")

    @log_level.setter
    def log_level(self, value):
        """Set the log_level setting"""
        self._set_option("log_level", value)

    @property
    def root_dir(self):
        """Get the root dir setting"""
        return self._get_option("root_dir")

    @root_dir.setter
    def root_dir(self, value):
        """Set the root_dir setting"""
        self._set_option("root_dir", value)

    @property
    def tenant(self):
        """Get the tenant setting"""
        return self._get_option("tenant")

    @tenant.setter
    def tenant(self, value):
        """Set the tenant setting"""
        self._set_option("tenant", value)

    @property
    def account(self):
        """Get the account setting"""
        return self._get_option("account")

    @account.setter
    def account(self, value):
        """Set the account setting"""
        self._set_option("account", value)

    @property
    def product(self):
        """Get the product setting"""
        return self._get_option("product")

    @product.setter
    def product(self, value):
        """Set the product setting"""
        self._set_option("product", value)

    @property
    def environment(self):
        """Get the environment setting"""
        return self._get_option("environment")

    @environment.setter
    def environment(self, value):
        """Set the environment setting"""
        self._set_option("environment", value)

    @property
    def segment(self):
        """Get the segment setting"""
        return self._get_option("segment")

    @segment.setter
    def segment(self, value):
        """Set the segment setting"""
        self._set_option("segment", value)

    @property
    def engine(self):
        """Get the engine to use for the district"""
        return self._get_option("engine")

    @engine.setter
    def engine(self, value):
        """Set the engine setting"""
        self._set_option("engine", value)

    @property
    def engine_update_install(self):
        """Handle how engine updates are handled"""
        return self._get_option("engine_update_install")

    @engine_update_install.setter
    def engine_update_install(self, value):
        """Set the engine_update_install setting"""
        self._set_option("engine_update_install", value)

    @property
    def engine_update_interval(self):
        """How often to check for updates to active engine"""
        return self._get_option("engine_update_interval")

    @engine_update_interval.setter
    def engine_update_interval(self, value):
        """How often to check for updates to active engine"""
        self._set_option("engine_update_interval", value)

    @property
    def generation_framework(self):
        """Get the generation_framework setting"""
        return self._get_option("generation_framework")

    @generation_framework.setter
    def generation_framework(self, value):
        """Set the generation_framework setting"""
        self._set_option("generation_framework", value)

    @property
    def generation_provider(self):
        """Get the generation_provider setting"""
        return self._get_option("generation_provider")

    @generation_provider.setter
    def generation_provider(self, value):
        """Set the generation_provider setting"""
        self._set_option("generation_provider", value)

    @property
    def generation_input_source(self):
        """Get the generation_input_source setting"""
        return self._get_option("generation_input_source")

    @generation_input_source.setter
    def generation_input_source(self, value):
        """Set the generation_input_source setting"""
        self._set_option("generation_input_source", value)

    def _get_option(self, name, default=None):
        """Get value for an option."""
        value = self.opts.get(name)
        if value is None:
            return default
        return value

    def _set_option(self, name, value, allow_clear=False):
        """Set value for an option."""
        if not allow_clear:
            # Prevent clears if value was set
            try:
                current_value = self._get_option(name)
                if value is None and current_value is not None:
                    return
            except AttributeError:
                pass
        self.opts[name] = value


pass_options = click.make_pass_decorator(Options, ensure=True)
