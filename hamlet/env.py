import os
import click


HAMLET_HOME_DIR = os.environ.get(
    'HAMLET_HOME_DIR',
    click.get_app_dir(app_name='hamlet', force_posix=True, roaming=False)
)
ENGINE_ENV = {
    'GENERATION_DIR': os.environ.get('GENERATION_DIR')
}


def set_engine_env(env):
    '''
    Used by child processes to update the env global as required
    '''
    global ENGINE_ENV
    ENGINE_ENV = env
