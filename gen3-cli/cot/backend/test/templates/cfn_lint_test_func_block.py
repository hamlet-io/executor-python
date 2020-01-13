# NOTE: this file must remain valid python file in order to perform tests on it


def cfn_lint_test(filename):
    import json
    import subprocess
    cmd = ' '.join([
        'cfn-lint',
        '-f',
        'json',
        filename
    ])
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf8'
    )
    if result.stderr:
        raise Exception(result.stderr)
    else:
        errors = json.loads(result.stdout)
        if errors:
            raise AssertionError(json.dumps(errors, indent=4))
