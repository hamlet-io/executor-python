import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.schema import create_schemas as create_schemas
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'unit'
ALL_VALID_OPTIONS['!-l,--deployment-group'] = 'group'
ALL_VALID_OPTIONS['!-o,--output-dir'] = 'output_dir'

@mock.patch('hamlet.command.schema.create_schema_backend')
def test_input_valid(create_schema_backend):
    run_options_test(CliRunner(), create_schemas, ALL_VALID_OPTIONS, create_schema_backend.run)

@mock.patch('hamlet.command.schema.create_schema_backend')
def test_input_validation(create_schema_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        create_schemas,
        create_schema_backend.run,
        {
            '-l': 'component',
            '-u': 'baseline',
            '-o': '.'
        },
        [
            ('-l', 'notavalidvalue', 'component'),
            ('-u', 'not_valid', 'baseline')
        ]
    )