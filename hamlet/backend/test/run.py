import subprocess
import shutil
from pytest import ExitCode as ec

from hamlet.backend.common.exceptions import BackendException


def run(testpaths=None, root_dir=None, pytest_args=None, silent=True):
    testpaths = testpaths or []
    # Do not use pytest.main because it can't correctly work with the files changed in runtime

    if shutil.which("bash") is None:
        raise BackendException("Could not find bash installation")

    try:
        args = [
            "pytest",
            "-vvs" if not silent else "",
            "--cache-clear",
        ]

        if root_dir is not None:
            args.append(f"--rootdir={root_dir}")

        if pytest_args is not None:
            args.append(pytest_args)

        args += [
            *testpaths,
        ]

        cmd = " ".join(args)
        stdin = subprocess.PIPE
        stderr = subprocess.PIPE
        process = subprocess.Popen(
            [shutil.which("bash"), "-c", cmd],
            stdin=stdin,
            stderr=stderr,
            start_new_session=True,
            cwd=root_dir,
        )
        process.wait()
        if process.returncode in [ec.OK, ec.NO_TESTS_COLLECTED]:
            return True
        if process.returncode == ec.TESTS_FAILED:
            raise Exception("Tests Failed")
        if process.returncode in [ec.INTERNAL_ERROR, ec.USAGE_ERROR, ec.TESTS_FAILED]:
            raise Exception(process.stderr)
        else:
            raise Exception("Unknown exit code: %s" % process.returncode)
    finally:
        process.kill()
