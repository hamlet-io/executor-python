import os
import shutil
import pytest
from unittest import mock
from hamlet.loggers import logging, root
from hamlet.backend.engine import EngineStore
from hamlet.command.common.config import Options


root.setLevel(logging.DEBUG)


class __CMDBContext:
    if os.getenv("TEST_ROOT_DIR", None) is not None:
        ROOT_DIR = os.getenv("TEST_ROOT_DIR")
    else:
        ROOT_DIR = os.getcwd() + "/.cmdb"
        os.makedirs(ROOT_DIR, exist_ok=True)

    def create_cmdb_filename_compositor(self):
        root = self.dir

        def cmdb_filename_compositor(*args, sep="-", ext=""):
            name = sep.join([*args])
            filename = os.path.join(root, name)
            if ext:
                filename += ".%s" % ext
            return os.path.normpath(filename)

        return cmdb_filename_compositor

    def __init__(self, *args):
        self.dir = os.path.join(self.ROOT_DIR, *args)
        self.old_cwd = os.getcwd()

    def __enter__(self):
        assert os.path.exists(self.dir), "Path %s does not exit" % self.dir
        assert os.path.isdir(self.dir), "Path %s is not a dir" % self.dir
        os.chdir(self.dir)
        return self.create_cmdb_filename_compositor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)


def __clear_dir(dir):
    assert os.path.isdir(dir)
    for entry in os.listdir(dir):
        entry = os.path.abspath(os.path.join(dir, entry))
        if os.path.isdir(entry):
            shutil.rmtree(entry)
        else:
            os.remove(entry)


def __clear_cmdb(*args):
    with __CMDBContext() as path:
        if not args:
            __clear_dir(path())
        else:
            __clear_dir(os.path.join(*args))


@pytest.fixture(scope="session")
def cmdb():
    return __CMDBContext


@pytest.fixture(scope="session")
def clear_cmdb():
    return __clear_cmdb


class __EngineContext:
    def __init__(self) -> None:
        if os.getenv("TEST_ENGINE_STORE_DIR", None) is not None:
            ENGINE_STORE_DIR = os.getenv("TEST_ENGINE_STORE_DIR")
        else:
            ENGINE_STORE_DIR = os.getcwd() + "/.engine_store"
            os.makedirs(ENGINE_STORE_DIR, exist_ok=True)

        self._engine_store = EngineStore(
            store_dir=ENGINE_STORE_DIR, config_search_paths=ENGINE_STORE_DIR
        )
        self._engine_store.load_engines(locations=["local", "remote"], refresh=True)
        self._engine_store.get_engine("unicycle", ["remote"]).install()
        self._engine_store.load_engines(locations=["installed"], refresh=True)

        self._engine = self._engine_store.get_engine("unicycle", ["installed"])

    @property
    def engine(self):
        return self._engine

    @property
    def engine_store(self):
        return self._engine_store


@pytest.fixture(scope="session")
def engine():
    return __EngineContext()


def mock_engine():
    engine = mock.MagicMock()
    engine.name = mock.PropertyMock().return_value = "Name[1]"
    engine.location = mock.PropertyMock().return_value = "local"
    engine.description = mock.PropertyMock().return_value = "Description[1]"
    engine.short_digest = mock.PropertyMock().return_value = "Digest[1]"
    engine.digest = mock.PropertyMock().return_value = "Digest[1]"
    return engine


def mock_engine_store():
    engine_store = mock.MagicMock()
    engine_store.get_engines.return_value = [mock_engine()]
    return engine_store


class __Options(Options):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._engine = mock_engine()
        self._engine_store = mock_engine_store()


@pytest.fixture(scope="session")
def options():
    return __Options()


def __clear_engine(*args):
    if os.path.exists(__EngineContext.ENGINE_STORE_DIR) and os.path.isdir(
        __EngineContext.ENGINE_STORE_DIR
    ):
        shutil.rmtree(__EngineContext.ENGINE_STORE_DIR)


@pytest.fixture(scope="session")
def clear_engine():
    return __clear_engine
