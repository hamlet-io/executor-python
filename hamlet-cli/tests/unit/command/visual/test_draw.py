import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.visual import draw_diagram as draw_diagram
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['!-l,--level'] = 'level'
ALL_VALID_OPTIONS['-x,--disable-output-cleanup'] = [True]
ALL_VALID_OPTIONS['-o,--output-dir'] = 'output_dir'


@mock.patch('hamlet.command.visual.create_template_backend')
def test_input_valid(create_template_backend):
    run_options_test(CliRunner(), draw_diagram, ALL_VALID_OPTIONS, create_template_backend.run)


@mock.patch('hamlet.command.visual.create_template_backend')
def test_input_validation(create_template_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        draw_diagram,
        create_template_backend.run,
        {
            '-l': 'overview'
        },
        []
    )
