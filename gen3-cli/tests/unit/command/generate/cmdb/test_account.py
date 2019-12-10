from unittest import mock
from click.testing import CliRunner
from cot.command.generate.cmdb import generate_account
from tests.unit.command.generate.utils import inputlines


@mock.patch('cot.command.generate.cmdb.generate_account_backend')
def test(generate_account_backend):
    generate_account_backend.generate_account_seed.return_value = 'random'
    runner = CliRunner()
    result = runner.invoke(
        generate_account,
        [
            '--account-id',
            'account-id'
        ]
    )
    assert result.exit_code == 0, result.output
    assert generate_account_backend.run.call_count == 1

    generate_account_backend.run.assert_called_once_with(
        account_id='account-id',
        account_name='account-id',
        account_seed='random',
        account_type='aws',
        aws_account_id=''
    )

    generate_account_backend.reset_mock()
    result = runner.invoke(
        generate_account,
        [
            '--account-id',
            'id',

            '--account-name',
            'name',

            '--account-seed',
            'not_random',

            '--account-type',
            'type',

            '--aws-account-id',
            'None'
        ]
    )
    assert result.exit_code == 0, result.output
    generate_account_backend.run.assert_called_once_with(
        account_id='id',
        account_name='name',
        account_seed='not_random',
        account_type='type',
        aws_account_id='None'
    )

    generate_account_backend.reset_mock()
    result = runner.invoke(
        generate_account,
        [
            '--prompt'
        ],
        input=inputlines(
            'id',
            'name',
            'not_random',
            'type',
            'None',
            'y'
        )
    )
    assert result.exit_code == 0, result.output
    generate_account_backend.run.assert_called_once_with(
        account_id='id',
        account_name='name',
        account_seed='not_random',
        account_type='type',
        aws_account_id='None'
    )

    generate_account_backend.reset_mock()
    result = runner.invoke(
        generate_account,
        [
            '--prompt',
            '--use-default'
        ],
        input=inputlines(
            'account-id',
            'y'
        )
    )
    assert result.exit_code == 0, result.output
    generate_account_backend.run.assert_called_once_with(
        account_id='account-id',
        account_name='account-id',
        account_seed='random',
        account_type='aws',
        aws_account_id=''
    )
