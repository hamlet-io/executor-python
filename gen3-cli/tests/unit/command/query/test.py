import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.query import query
from tests.unit.command.test_option_generation import run_options_test


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS['-p,--blueprint-generation-provider'] = 'generation_provider'
ALL_VALID_OPTIONS['-f,--blueprint-generation-framework'] = 'generation_framework'
ALL_VALID_OPTIONS['-i,--blueprint-generation-input-source'] = 'input-source'
ALL_VALID_OPTIONS['-s,--blueprint-generation-scenarios'] = 'generation_scenarious'
ALL_VALID_OPTIONS['-q,--query'] = 'query'
ALL_VALID_OPTIONS['-t,--list-tiers'] = [True, False]
ALL_VALID_OPTIONS['-c,--list-components'] = [True, False]
ALL_VALID_OPTIONS['-r,--blueprint-refresh'] = [True, False]


@mock.patch('cot.command.query.query_backend')
def test_input_valid(query_backend):
    run_options_test(CliRunner(), query, ALL_VALID_OPTIONS, query_backend.run)
