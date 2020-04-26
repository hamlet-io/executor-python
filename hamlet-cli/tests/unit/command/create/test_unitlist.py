import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.create.unitlist import unitlist as create_unitlist
from tests.unit.command.test_option_generation import run_options_test


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['-p,--generation-provider'] = 'generation_provider'
ALL_VALID_OPTIONS['-f,--generation-framework'] = 'generation_framework'
ALL_VALID_OPTIONS['-i,--generation-input-source'] = 'input-source'
ALL_VALID_OPTIONS['-o,--output-dir'] = '/tmp'


@mock.patch('hamlet.command.create.unitlist.create_unitlist_backend')
def test_input_valid(create_unitlist_backend):
    run_options_test(CliRunner(), create_unitlist, ALL_VALID_OPTIONS, create_unitlist_backend.run)
