from unittest import mock
from click.testing import CliRunner
from cot.command.generate.product import generate_base
from tests.unit.command.generate.utils import inputlines


@mock.patch('cot.command.generate.product.generate_base_backend')
def test(generate_base_backend):
    runner = CliRunner()
    result = runner.invoke(
        generate_base,
        [
            '--product-id',
            'base-id',
            '--solution-id',
            'solution-id',
            '--environment-id',
            'environment-id'
        ]
    )
    assert result.exit_code == 0, result.output
    generate_base_backend.run.assert_called_once_with(
        product_id='base-id',
        product_name='base-id',
        domain_id='',
        solution_id='solution-id',
        solution_name='solution-id',
        environment_id='environment-id',
        environment_name='environment-id',
        segment_id='default',
        segment_name='default'
    )

    generate_base_backend.reset_mock()
    result = runner.invoke(
        generate_base,
        [
            '--product-id',
            'base-id',

            '--product-name',
            'base-name',

            '--domain-id',
            'domain-id',

            '--solution-id',
            'solution-id',

            '--solution-name',
            'solution-name',

            '--environment-id',
            'environment-id',

            '--environment-name',
            'environment-name',

            '--segment-id',
            'segment-id',

            '--segment-name',
            'segment-name'
        ]
    )

    assert result.exit_code == 0, result.output
    generate_base_backend.run.assert_called_once_with(
        product_id='base-id',
        product_name='base-name',
        domain_id='domain-id',
        solution_id='solution-id',
        solution_name='solution-name',
        environment_id='environment-id',
        environment_name='environment-name',
        segment_id='segment-id',
        segment_name='segment-name'
    )

    generate_base_backend.reset_mock()
    result = runner.invoke(
        generate_base,
        [
            '--prompt'
        ],
        input=inputlines(
            'base-id',
            'base-name',
            'domain-id',
            'solution-id',
            'solution-name',
            'environment-id',
            'environment-name',
            'segment-id',
            'segment-name',
            'y'
        )
    )
    assert result.exit_code == 0, result.output
    generate_base_backend.run.assert_called_once_with(
        product_id='base-id',
        product_name='base-name',
        domain_id='domain-id',
        solution_id='solution-id',
        solution_name='solution-name',
        environment_id='environment-id',
        environment_name='environment-name',
        segment_id='segment-id',
        segment_name='segment-name'
    )

    generate_base_backend.reset_mock()
    result = runner.invoke(
        generate_base,
        [
            '--prompt',
            '--use-default'
        ],
        input=inputlines(
            'base-id',
            'solution-id',
            'environment-id',
            'y'
        )
    )
    assert result.exit_code == 0, result.output
    generate_base_backend.run.assert_called_once_with(
        product_id='base-id',
        product_name='base-id',
        domain_id='',
        solution_id='solution-id',
        solution_name='solution-id',
        environment_id='environment-id',
        environment_name='environment-id',
        segment_id='default',
        segment_name='default'
    )
