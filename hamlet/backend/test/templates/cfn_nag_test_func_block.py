# NOTE: this file must remain valid python file in order to perform tests on it


def cfn_nag_test(filename):
    import json
    import subprocess

    cmd = " ".join(
        ["cfn_nag_scan", "--output-format", "json", "--input-path", filename]
    )
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8"
    )
    if result.stderr:
        raise Exception(result.stderr)
    else:
        errors = json.loads(result.stdout)[0]["file_results"]["violations"]
        errors = list(e for e in errors if e["type"] != "WARN")
        if errors:
            raise AssertionError(json.dumps(errors, indent=4))
