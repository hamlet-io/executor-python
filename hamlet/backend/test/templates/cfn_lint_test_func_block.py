# NOTE: this file must remain valid python file in order to perform tests on it


def cfn_lint_test(filename, ignore_checks=None):
    import json
    import subprocess

    cmd_args = ["cfn-lint", "-f", "json", filename]

    if ignore_checks is not None:
        cmd_args.append("--ignore-checks")
        cmd_args.append(" ".join(ignore_checks))

    result = subprocess.run(
        cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8"
    )
    if result.stderr:
        raise Exception(result.stderr)
    else:
        errors = json.loads(result.stdout)
        if errors:
            raise AssertionError(json.dumps(errors, indent=4))
