import os
import click


ENGINE_ENV = {"GENERATION_DIR": os.environ.get("GENERATION_DIR")}

HAMLET_HOME_DIR = os.environ.get(
    "HAMLET_HOME_DIR",
    click.get_app_dir(app_name="hamlet", force_posix=True, roaming=False),
)
HAMLET_CONFIG_DIR = os.path.join(HAMLET_HOME_DIR, "config")


def set_engine_env(env):
    """
    Used by child processes to update the env global as required
    """
    global ENGINE_ENV
    ENGINE_ENV = env


def set_cli_config_dir(dir):
    """
    Used by child processes to update the hamlet config dir
    """

    global HAMLET_CONFIG_DIR
    HAMLET_CONFIG_DIR = dir
