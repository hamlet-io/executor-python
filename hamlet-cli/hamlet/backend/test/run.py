import subprocess
from pytest import ExitCode as ec


def run(
    testpaths=None,
    pytest_args=None,
    silent=True
):
    testpaths = testpaths or []
    # Do not use pytest.main because it can't correctly work with the files changed in runtime
    try:
        args = [
            'pytest',
            '-vvs' if not silent else '',
            '--cache-clear',
        ]

        if pytest_args is not None:
            args.append(pytest_args)

        args += [
            *testpaths,
        ]

        cmd = " ".join(args)
        stdin = subprocess.PIPE
        stderr = subprocess.PIPE
        process = subprocess.Popen(
            [
                '/bin/bash',
                '-c',
                cmd
            ],
            stdin=stdin,
            stderr=stderr,
            start_new_session=True
        )
        process.wait()
        if process.returncode in [ec.OK, ec.NO_TESTS_COLLECTED]:
            return True
        if process.returncode == ec.TESTS_FAILED:
            raise Exception('Tests Failed')
        if process.returncode in [ec.INTERNAL_ERROR, ec.USAGE_ERROR, ec.TESTS_FAILED]:
            raise Exception(process.stderr)
        else:
            raise Exception("Unknown exit code: %s" % process.returncode)
    finally:
        process.kill()
