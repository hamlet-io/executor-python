import os

from hamlet.env import HAMLET_HOME_DIR

ENGINE_STORE_DIR = os.path.join(HAMLET_HOME_DIR, 'engine')
ENGINE_STORE_ENGINES_DIR = os.path.join(ENGINE_STORE_DIR, 'engines')
ENGINE_STORE_ENGINE_STATE_FILENAME = 'engine_state.json'
ENGINE_GLOBAL_NAME = '_global'
