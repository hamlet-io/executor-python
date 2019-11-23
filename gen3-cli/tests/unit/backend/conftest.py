import os
import pytest


class CMDBContext:

    ROOT_DIR = '/var/opt/codeontap'

    def __init__(self, dir):
        self.dir = os.path.join(self.ROOT_DIR, dir)
        self.old_cwd = os.getcwd()

    def __enter__(self):
        os.chdir(self.dir)
        return self.dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)


@pytest.fixture(scope='session')
def cmdb():
    return CMDBContext
