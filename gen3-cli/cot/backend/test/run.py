import pytest
from pytest import ExitCode


def run(*testpaths):
    args = [
        '--cache-clear',
        *testpaths,
    ]
    exit_code = pytest.main(args)
    if exit_code in [ExitCode.OK, ExitCode.NO_TESTS_COLLECTED]:
        return True
    elif exit_code == ExitCode.TESTS_FAILED:
        return False
    elif exit_code in [ExitCode.INTERRUPTED, ExitCode.USAGE_ERROR, ExitCode.INTERNAL_ERROR]:
        raise Exception(str(exit_code))
