import os
import json
from click.testing import CliRunner
from .command import run_cmd, test_cmd


def datafile(filename):
    return os.path.join('/gen3-cli/tests/data/system/testcases', filename)


def test_run_cmd():
    runner = CliRunner()
    result = runner.invoke(
        run_cmd,
        [
            '-f',
            datafile('testcase-success.yml')
        ]
    )
    assert json.loads(result.output).get('status') == 'PASSED'
    assert result.exit_code == 0

    result = runner.invoke(
        run_cmd,
        [
            '-f',
            datafile('testcase-failed.yml'),
        ]
    )
    assert json.loads(result.output).get('status') == 'FAILED'
    assert result.exit_code == 1
    with runner.isolated_filesystem():
        result = runner.invoke(
            run_cmd,
            [
                '-f',
                datafile('testcase-success.yml'),
                '-f',
                datafile('testcase-failed.yml'),
                '-o',
                'test-results.json',
                '-v'
            ]
        )
        assert result.exit_code == 1, result.output
        with open('test-results.json', 'rb') as f:
            output = json.load(f)
            assert len(output['results']) == 2
            assert output['results']['testSuccess']['status'] == 'PASSED'
            assert output['results']['testFailed']['status'] == 'FAILED'


def test_test_cmd():
    runner = CliRunner()
    result = runner.invoke(
        test_cmd,
        [
            '--file',
            datafile('valid-syntax-cf.yml'),

            '--match',
            'Parameters.ApplicationName.Type',
            'String',

            '--match',
            'Parameters.Environment.AllowedValues.0',
            'Dev',

            '--match',
            'Resources.untaggedInstance',
            '{"Type":"AWS::EC2::Instance","Properties":{"ImageId":"ami-123456"}}',

            '--length',
            'Parameters.Environment.AllowedValues',
            '2',

            '--exists',
            'Parameters.Environment.AllowedValues.0',

            '--not-empty',
            'Resources',

            '--resource',
            'untaggedInstance',
            'AWS::EC2::Instance'
        ]
    )
    assert result.exit_code == 0, result.output
