import os
import json
import subprocess


def find_linter_errors(filename):
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
        return errors


def find_potential_vulnerabilities(filename, ignore_warn=True):
    cmd = ' '.join([
        'cfn_nag_scan',
        '--output-format',
        'json',
        '--input-path',
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
        errors = json.loads(result.stdout)[0]['file_results']['violations']
        if ignore_warn:
            errors = list(e for e in errors if e['type'] != 'WARN')
        return errors


DATA_PATH = 'tests/data/system/testcases'


# just a quick tests to check that everything is working
def test_find_linter_errors():
    assert not find_linter_errors(os.path.join(DATA_PATH, 'valid-syntax-cf.yml'))
    assert find_linter_errors(os.path.join(DATA_PATH, 'invalid-syntax-cf.yml'))


# another quick test
def test_find_potential_vulnerabilities():
    assert not find_potential_vulnerabilities(os.path.join(DATA_PATH, 'secure-cf.yml'))
    assert find_potential_vulnerabilities(os.path.join(DATA_PATH, 'secure-cf.yml'), ignore_warn=False)
    assert find_potential_vulnerabilities(os.path.join(DATA_PATH, 'insecure-cf.yml'))
