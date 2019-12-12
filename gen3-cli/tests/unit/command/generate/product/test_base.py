import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.generate.product import generate_base
from tests.unit.command.generate.test_generate_command import run_generate_command_test

OPTIONS = collections.OrderedDict()
OPTIONS['!--product-id,product_id'] = 'test-product-id'
OPTIONS['--product-name,product_name'] = ('test-product-name', 'test-product-id')
OPTIONS['--domain-id,domain_id'] = ('test-domain-id', '')
OPTIONS['!--solution-id,solution_id'] = 'test-solution-id'
OPTIONS['--solution-name,solution_name'] = ('test-solution-name', 'test-solution-id')
OPTIONS['!--environment-id,environment_id'] = 'test-environment-id'
OPTIONS['--environment-name,environment_name'] = ('test-environment-name', 'test-environment-id')
OPTIONS['--segment-id,segment_id'] = ('test-segment-id', 'default')
OPTIONS['--segment-name,segment_name'] = ('test-segment-name', 'default')


@mock.patch('cot.command.generate.product.generate_base_backend')
def test(generate_base_backend):
    run_generate_command_test(
        CliRunner(),
        generate_base,
        generate_base_backend.run,
        OPTIONS
    )
