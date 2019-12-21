import os
import tempfile
import pytest
from cot.backend.test.templates.cf_structure_obj_block import (
    Structure,
    structure_test
)
from cot.backend.test.templates.cf_test_lint_func_block import lint_test
from cot.backend.test.templates.cf_test_vulnerability_func_block import vulnerability_test
from .conftest import DATA_DIR

CF_TEMPLATES_PATH = os.path.join(DATA_DIR, 'cf')


def test_vulnerability_test():
    vulnerability_test(os.path.join(CF_TEMPLATES_PATH, 'secure.json'))
    with pytest.raises(AssertionError):
        vulnerability_test(os.path.join(CF_TEMPLATES_PATH, 'insecure.json'))


def test_lint_test():
    lint_test(os.path.join(CF_TEMPLATES_PATH, 'valid-syntax.json'))
    with pytest.raises(AssertionError):
        lint_test(os.path.join(CF_TEMPLATES_PATH, 'invalid-syntax.json'))


def test_structure_object():
    body = {
        'path': {
            'exists': []
        },
        'not': {
            'empty': {
                'list': [1, 2],
                'scalar': 1,
                'obj': {
                    '1': 'value',
                    '2': 'value',
                    '3': 'value'
                }
            }
        },
        'empty': {
            'list': [],
            'scalar': None,
            'obj': {}
        },
        Structure.RESOURCES_KEY: {
            'TestResource': {
                Structure.RESOURCE_TYPE_KEY: 'TestType'
            }
        },
        Structure.OUTPUT_KEY: {
            'TestOutput': {
                'Value': 'value'
            }
        }
    }
    template = Structure(body)

    template.match('path.exists', [])

    template.resource('TestResource', 'TestType')

    template.output('TestOutput')

    template.len('not.empty.list', 2)
    template.len('not.empty.obj', 3)

    template.exists('path.exists')

    template.not_empty('not.empty.list')
    template.not_empty('not.empty.scalar')
    template.not_empty('not.empty.obj')
    assert not template.errors

    template = Structure(body)
    template.match('path.exists', [1])
    template.match('not.empty.scalar', 10)
    template.match('not.empty.obj', {'1': 'value'})
    assert len(template.errors) == 3

    template = Structure(body)
    template.resource('NotExists', 'TestType')
    template.resource('TestResource', 'WrongType')
    assert len(template.errors) == 2

    template = Structure(body)
    template.output('NotExists')
    assert len(template.errors) == 1

    template = Structure(body)
    template.len('not.empty.list', 3)
    template.len('not.empty.obj', 2)
    assert len(template.errors) == 2

    template = Structure(body)
    template.exists('not.path.exists')
    assert len(template.errors) == 1

    template = Structure(body)
    template.not_empty('empty.list')
    template.not_empty('empty.scalar')
    template.not_empty('empty.obj')
    assert len(template.errors) == 3


def test_structure_test():
    structure = structure_test(os.path.join(CF_TEMPLATES_PATH, 'valid-syntax.json'))
    structure.output("DOES NOT EXITS")
    with pytest.raises(AssertionError):
        structure.assert_structure()
    with pytest.raises(AssertionError):
        structure = structure_test(os.path.join(CF_TEMPLATES_PATH, 'not-exists.json'))
    with tempfile.TemporaryDirectory() as dir:
        filename = os.path.join(dir, 'test.txt')
        with open(filename, 'wt+') as f:
            f.write("Not a json")
        with pytest.raises(AssertionError):
            structure = structure_test(filename)

    structure = structure_test(os.path.join(CF_TEMPLATES_PATH, 'valid-syntax.json'))
    structure.exists('Resources')
    structure.assert_structure()
