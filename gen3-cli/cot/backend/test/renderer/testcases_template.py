import json
from ..loader import loader


def prepare_cf_testcase_context(case):
    structure = case.get('structure', {})
    match = structure.get('match', [])
    stringified_match = []
    for path, value in match:
        try:
            value = json.loads(value)
        except ValueError:
            value = "\"{}\"".format(value)
        except TypeError:
            pass
        stringified_match.append((path, value))

    if structure:
        if match:
            structure['match'] = stringified_match


def prepare_context(cases):
    test_lint = False
    test_structure = False
    test_vulnerability = False
    prepared_cases = list()
    ordered_casenames = list(cases.keys())
    ordered_casenames.sort()
    for casename in ordered_casenames:
        data = cases[casename]
        type = None
        if data['filename'].endswith('.json'):
            type = 'cf'
        if type == 'cf':
            prepare_cf_testcase_context(data)
            if not data.get('no_lint', False):
                test_lint = True
            if not data.get('no_vulnerability_check', False):
                test_vulnerability = True
            if data.get('structure', False):
                test_structure = True
        prepared_cases.append((casename, data, type))
    return {
        "test_lint": test_lint,
        "test_structure": test_structure,
        "test_vulnerability": test_vulnerability,
        "cases": prepared_cases
    }


def render(cases=None):
    context = prepare_context(cases)
    template = loader.get_template('test_template_base.py.tmpl')
    return template.render(**context)
