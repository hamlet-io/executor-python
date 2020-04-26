import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.create.buildblueprint import buildblueprint as create_buildblueprint
from tests.unit.command.test_option_generation import run_options_test


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['!-u,--deployment-unit'] = 'deployment_unit'
ALL_VALID_OPTIONS['-p,--generation-provider'] = 'generation_provider'
ALL_VALID_OPTIONS['-f,--generation-framework'] = 'generation_framework'
ALL_VALID_OPTIONS['-i,--generation-input-source'] = 'input-source'
ALL_VALID_OPTIONS['-o,--output-dir'] = '/tmp'


@mock.patch('hamlet.command.create.buildblueprint.create_buildblueprint_backend')
def test_input_valid(create_buildblueprint_backend):
    run_options_test(CliRunner(), create_buildblueprint, ALL_VALID_OPTIONS, create_buildblueprint_backend.run)
