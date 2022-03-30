import click

from click_configfile import ConfigFileReader, SectionSchema, matches_section
from hamlet.utils import ConfigParam

from hamlet.backend.engine.exceptions import (
    EngineStoreMissingEngineException,
)

from hamlet.backend.engine import EngineStore


class ConfigSchema(object):
    """Schema for standard configuration."""

    @matches_section("default")
    class CliConfig(SectionSchema):
        """base level configuration of the cli itself"""

        log_level = ConfigParam(
            name="log_level",
            type=click.Choice(
                ["fatal", "error", "warn", "info", "debug", "trace"],
                case_sensitive=False,
            ),
        )
        log_format = ConfigParam(
            name="log_format",
            type=click.Choice(["compact", "full"], case_sensitive=False),
        )

    @matches_section("profile:*")
    class Profile(SectionSchema):
        """Profile-specific configuration schema."""

        root_dir = ConfigParam(name="root_dir", type=click.Path())
        district_type = ConfigParam(name="district_type", type=str)
        tenant = ConfigParam(name="tenant", type=str)
        account = ConfigParam(name="account", type=str)
        product = ConfigParam(name="product", type=str)
        environment = ConfigParam(name="environment", type=str)
        segment = ConfigParam(name="segment", type=str)
        engine = ConfigParam(name="engine", type=str)


class ConfigReader(ConfigFileReader):
    """Reader for standard configuration."""

    config_files = ["config.ini", "config"]
    config_name = "standard"
    config_section_schemas = [ConfigSchema.Profile, ConfigSchema.CliConfig]

    @classmethod
    def select_config_schema_for(cls, section_name):
        section_schema = super(ConfigReader, cls).select_config_schema_for(section_name)
        for v in section_schema.__dict__:
            if isinstance(v, ConfigParam):
                v.ctx = cls
        return section_schema

    @classmethod
    def read_config(cls, config_searchpath):
        cls.config_searchpath = config_searchpath
        return super().read_config()

    def load_config(self, opts, profile=None):
        """Load a configuration file into an options object."""
        config = self.read_config(self.config_searchpath)
        values = config.get("default", {})
        self._load_values_into_opts(opts, values)

        if profile:
            values = config.get(f"profile:{profile}", {})
            self._load_values_into_opts(opts, values)

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

        self.default_engine_name = "train"
        self._engine_store = None
        self._engine = None

    def get_config_reader(self):
        """Get the config reader class."""
        return ConfigReader()

    def load_config_file(self, profile=None, searchpath=None):
        """Load the config file."""
        config_cls = self.get_config_reader()
        if searchpath:
            config_cls.config_searchpath = [searchpath]
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
    def hamlet_home_dir(self):
        """The home dir used by hamlet"""
        return self._get_option("hamlet_home_dir")

    @hamlet_home_dir.setter
    def hamlet_home_dir(self, value):
        """set the hamlet home dir"""
        self._set_option("hamlet_home_dir", value)

    @property
    def cli_cache_dir(self):
        """The cli cache dir"""
        return self._get_option("cli_cache_dir")

    @cli_cache_dir.setter
    def cli_cache_dir(self, value):
        """Set the cli cache dir"""
        self._set_option("cli_cache_dir", value)

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
    def district_type(self):
        """Get the district type setting"""
        return self._get_option("district_type")

    @district_type.setter
    def district_type(self, value):
        """Set the district type setting"""
        self._set_option("district_type", value)

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

    @property
    def engine_store(self):
        return self._engine_store

    @property
    def engine(self):
        return self._engine

    def set_engine_store(self, engine_dir, config_search_paths):
        self._engine_store = EngineStore(
            store_dir=engine_dir, config_search_paths=config_search_paths
        )

    def set_engine(self, engine_name, locations):
        if self.engine_store:
            engine_name = (
                engine_name
                or self.engine_store.default_engine
                or self.default_engine_name
            )

            try:
                self.engine_store.load_engines(locations=["installed"])
                self._engine = self.engine_store.get_engine(
                    engine_name, locations=["installed"]
                )

            except EngineStoreMissingEngineException:
                self.engine_store.load_engines(locations=locations)
                self.engine_store.get_engine(engine_name, locations=locations).install()
                self.engine_store.load_engines(locations=["installed"], refresh=True)

                self._engine = self.engine_store.get_engine(
                    engine_name, locations=["installed"]
                )


pass_options = click.make_pass_decorator(Options, ensure=True)
