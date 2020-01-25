import copy
import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.query import get, list_tiers, list_components
from tests.unit.command.test_option_generation import run_options_test


COMMON_VALID_OPTIONS = collections.OrderedDict()

COMMON_VALID_OPTIONS['-p,--blueprint-generation-provider'] = 'generation_provider'
COMMON_VALID_OPTIONS['-f,--blueprint-generation-framework'] = 'generation_framework'
COMMON_VALID_OPTIONS['-i,--blueprint-generation-input-source'] = 'input-source'
COMMON_VALID_OPTIONS['-s,--blueprint-generation-scenarios'] = 'generation_scenarious'
COMMON_VALID_OPTIONS['-r,--blueprint-refresh'] = [True, False]


@mock.patch('cot.command.query.query_backend')
def test_query_get_input(query_backend):
    query_backend.run.return_value = {'query': None}
    all_valid_options = copy.deepcopy(COMMON_VALID_OPTIONS)
    all_valid_options['!-q,--query'] = 'query'
    run_options_test(CliRunner(), get, all_valid_options, query_backend.run)


@mock.patch('cot.command.query.query_backend')
def test_query_list_tiers_input(query_backend):
    query_backend.run.return_value = {'tiers': []}
    run_options_test(CliRunner(), list_tiers, COMMON_VALID_OPTIONS, query_backend.run)


@mock.patch('cot.command.query.query_backend')
def test_query_list_components_input(query_backend):
    query_backend.run.return_value = {'components': []}
    run_options_test(CliRunner(), list_components, COMMON_VALID_OPTIONS, query_backend.run)
