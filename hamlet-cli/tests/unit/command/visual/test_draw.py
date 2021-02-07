import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.visual import draw_diagram as draw_diagram
from tests.unit.command.test_option_generation import run_options_test, run_validatable_option_test


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['!-t,--type'] = 'type'
ALL_VALID_OPTIONS['!-o,--output-dir'] = './'
ALL_VALID_OPTIONS['-x,--disable-output-cleanup'] = [True]


@mock.patch('hamlet.command.visual.create_diagram_backend')
@mock.patch('hamlet.command.visual.create_template_backend')
def test_input_valid(create_template_backend, create_diagram_backend):
    run_options_test(CliRunner(), draw_diagram, ALL_VALID_OPTIONS, create_template_backend.run)


@mock.patch('hamlet.command.visual.create_diagram_backend')
@mock.patch('hamlet.command.visual.create_template_backend')
def test_input_validation(create_template_backend, create_diagram_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        draw_diagram,
        create_template_backend.run,
        {
            '-t': 'overview',
            '-o': './'
        },
        []
    )
