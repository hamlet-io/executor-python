from ..loader import loader


def prepare_cf_testcase_context(case):
    json_structure = case.get("json_structure", {})
    match = json_structure.get("match", [])
    stringified_match = []
    for match_case in match:
        value = match_case["value"]
        if isinstance(value, str):
            value = value.replace('"', r"\"")
            value = value.replace("'", r"\'")
            value = f'"{value}"'
        stringified_match.append({"path": match_case["path"], "value": value})

    if json_structure:
        if match:
            json_structure["match"] = stringified_match


def prepare_context(cases):
    cfn_lint_test = False
    cfn_structure_test = False
    json_structure_test = False
    checkov_test = False
    prepared_cases = list()
    ordered_casenames = list(cases.keys())
    ordered_casenames.sort()
    for casename in ordered_casenames:
        data = cases[casename]
        type = None
        if data["filename"].endswith(".json"):
            type = "cf"
        if type == "cf":
            prepare_cf_testcase_context(data)
            cfn_lint_test = cfn_lint_test or "cfn_lint" in data
            checkov_test = checkov_test or "checkov" in data
            cfn_structure_test = cfn_structure_test or "cfn_structure" in data
            json_structure_test = json_structure_test or "json_structure" in data
        prepared_cases.append((casename, data, type))
    return {
        "checkov_test": checkov_test,
        "cfn_lint_test": cfn_lint_test,
        "json_validation_test": cfn_structure_test or json_structure_test,
        "cfn_structure_test": cfn_structure_test,
        "json_structure_test": json_structure_test,
        "cases": prepared_cases,
    }


def render(cases=None):
    context = prepare_context(cases)
    template = loader.get_template("test_template_base.py.tmpl")
    return template.render(**context)
