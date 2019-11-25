import os
import shutil
import pytest


class __CMDBContext:

    ROOT_DIR = '/var/opt/codeontap'

    def create_cmdb_filename_compositor(self):
        root = self.dir

        def cmdb_filename_compositor(*args, sep='-', ext=''):
            name = sep.join([*args])
            filename = os.path.join(root, name)
            if ext:
                filename += '.%s' % ext
            return filename
        return cmdb_filename_compositor

    def __init__(self, *args):
        self.dir = os.path.join(self.ROOT_DIR, *args)
        self.old_cwd = os.getcwd()

    def __enter__(self):
        assert os.path.exists(self.dir), 'Path %s does not exit' % self.dir
        assert os.path.isdir(self.dir), 'Path %s is not a dir' % self.dir
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


def __clear_cmdb_dir(*args):
    with __CMDBContext():
        __clear_dir(os.path.join(*args))


@pytest.fixture(scope='session')
def cmdb():
    return __CMDBContext


@pytest.fixture(scope='session')
def clear_cmdb_dir():
    return __clear_cmdb_dir
