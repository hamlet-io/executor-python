import os
import click


class GlobalEnvironmentConfig:
    """
    Handles Global Configuration which is used across hamlet
    """

    def __init__(self):
        self._home_dir = os.environ.get(
            "HAMLET_HOME_DIR",
            click.get_app_dir(app_name="hamlet", force_posix=True, roaming=False),
        )
        self._config_dir = os.environ.get(
            "HAMLET_CLI_CONFIG_DIR", os.path.join(self._home_dir, "config")
        )

        self._engine = None
        self._engine_env = {"GENERATION_DIR": os.environ.get("GENERATION_DIR")}

    @property
    def home_dir(self):
        return self._home_dir

    @property
    def config_dir(self):
        return self._config_dir

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine_name):
        self._engine = engine_name

    @property
    def engine_environment(self):
        return self._engine_env

    @engine_environment.setter
    def engine_environment(self, environment):
        self._engine_env = environment


HAMLET_GLOBAL_CONFIG = GlobalEnvironmentConfig()
