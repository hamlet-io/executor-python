import os

from hamlet.env import HAMLET_HOME_DIR

ENGINE_STORE_DEFAULT_DIR = os.path.join(HAMLET_HOME_DIR, "engine")
ENGINE_GLOBAL_NAME = "_global"
ENGINE_DEFAULT_GLOBAL_ENGINE = "train"
ENGINE_STATE_FILE_NAME = "engine_state.json"

ENGINE_STATE_VERSION = "1.0.1"
