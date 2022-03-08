# NOTE: this file must remain valid python file in order to perform tests on it


def checkov_test(filename, framework, skip_checks=None):
    import json
    import subprocess

    cmd_args = [
        "checkov",
        "--output",
        "json",
        "--framework",
        framework,
        "--quiet",
        "-f",
        filename,
    ]

    if skip_checks is not None:
        cmd_args.append("--skip-check")
        cmd_args.append(",".join(skip_checks))

    result = subprocess.run(
        cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8"
    )

    if result.returncode == 1:
        result = json.loads(result.stdout)
        if result["summary"]["failed"] >= 0:
            failure_details = []
            for detail in result["results"]["failed_checks"]:
                failure_details.append(
                    {
                        k: v
                        for k, v in detail.items()
                        if k
                        in [
                            "check_name",
                            "check_id",
                            "check_class",
                            "resource",
                            "guideline",
                            "check_result",
                        ]
                    }
                )
            raise AssertionError(json.dumps(failure_details, indent=4))

    if result.returncode >= 1:
        raise Exception(result.stderr)
