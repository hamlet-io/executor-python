import os
import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.create.reference import reference as create_reference
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test

ALL_VALID_OPTIONS = collections.OrderedDict()
ALL_VALID_OPTIONS['!-t,--reference-type'] = 'type'
ALL_VALID_OPTIONS['-o,--reference-output-dir'] = 'output_dir'


@mock.patch('cot.command.create.reference.create_reference_backend')
def test_input_valid(create_reference_backend):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir('output_dir')
        run_options_test(runner, create_reference, ALL_VALID_OPTIONS, create_reference_backend)


@mock.patch('cot.command.create.reference.create_reference_backend')
def test_input_validation(create_reference_backend):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir('output_dir')
        run_validatable_option_test(
            runner,
            create_reference,
            create_reference_backend,
            {
                '-t': 'type'
            },
            [
                ('-o', 'not_existing_dir', 'output_dir')
            ]
        )
