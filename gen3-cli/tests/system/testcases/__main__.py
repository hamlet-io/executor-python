#!/usr/bin/env python
import subprocess
import json
import yaml
from unittest import mock
import click
from cfn_flip import load_yaml
from test_generic_template_structure import Template
from test_generic_template import find_potential_vulnerabilities, find_linter_errors


class Echo:
    class Level:

        def __init__(self, echo, delta):
            self.echo = echo
            self.delta = delta

        def __enter__(self):
            self.old_level = self.echo._level
            self.echo._level += self.delta

        def __exit__(self, type, value, tb):
            self.echo._level = self.old_level

    def __init__(self, show):
        self._show = show
        self._level = 0

    def _dummy(*args, **kwargs):
        pass

    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        elif name.startswith('force_'):
            return object.__getattribute__(self, name[6:])
        else:
            if object.__getattribute__(self, '_show'):
                return object.__getattribute__(self, name)
            else:
                return object.__getattribute__(self, '_dummy')

    def level(self, delta=1):
        return self.Level(self, delta)

    def echo(self, text, fg=None):
        pad = self._level * "  "
        click.echo(click.style(pad + text, fg=fg))

    def info(self, text, alt=False):
        color = 'blue' if alt else 'cyan'
        self.echo(text, color)

    def success(self, text):
        self.echo(text, 'green')

    def error(self, text):
        self.echo(text, 'red')

    def warn(self, text):
        self.echo(text, 'yellow')


@click.group()
def root():
    pass


@root.command(
    name='run',
    short_help='run testcases defined in config file(s)',
    context_settings=dict(
        max_content_width=120
    )
)
@click.option(
    '-f',
    '--file',
    'config_filenames',
    multiple=True,
    required=True,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        exists=True
    ),
    help='Testcase config file. Multiple options will be composed into single conf.'
)
@click.option(
    '-o',
    '--output',
    'output_filename',
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True
    ),
    help='Output filename. If not provided output go to stdout'
)
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    help='Enables all potential outputs'
)
def run_testcases(config_filenames, output_filename, verbose):
    """
    Example usage:
    cot-testcases run -f config-1.yml -f config-2.yml -f config-3.yml -o test-results.json -v

    Runs testcases defined in config file(s).
    Can use yml and json configs.
    Can test yml and json CF templates.

    \b
    NOTE:
        CF YAML templates get converted to CF JSON format before testing.
        Pay attention when using match.

    \b
    Each test has 3 stages:
        1. cfn-lint test, results stored under lint key
        2. template structure test, results stored under structure key
        3. cfn-nag test, results stored under vulnerability key

    \b
    NOTE:
        If any of 3 stages fails testcase completes.
        Stages 1 and 3 can be disabled.

    \b
    Before each test you can specify set of setup instructions:
        cmd - command to be run
        env - env setup for that command

    \b
    NOTE:
        env resets after command completed.

    \b
    Most test props can be provided in compact way.
    YAML example:
        ---
            testCaseName:
                setup:
                    -
                        cmd: echo "hello $NAME"
                        env:
                            NAME: 'testCaseName'
                test:
                    match:
                        - [JSON.Property.Path, True]
                        -
                            - JSON.Property.Path
                            - True
                    resource:
                        - [TestResourceId, TestResourceType]
                        -
                            - TestResourceId
                            - TestResourceType
                    output:
                        - TestOutput
                        - AnotherTestOutput
                    output: [TestOutput, AnotherTestOutput]
                    length:
                        - [JSON.Path.Array, 10]
                        -
                            - JSON.Path.Array
                            - 10
                    exists:
                        - JSON.Property.Path.A
                        - JSON.Property.Path.B
                    exists: [JSON.Property.Path.A, JSON.Property.Path.B]
                    not_empty:
                        - JSON.Property.Path.A
                        - JSON.Property.Path
                    not_empty: [JSON.Property.Path.A, JSON.Property.Path.B]
                    no_lint: True
                    no_vulnerability_check: True

    \b
    Example JSON output:
        {
            "results": {
                "testCasePassed": {
                    "status": "PASSED",
                    "errors": null
                },
                "testCaseFailed": {
                    "status": "FAILED",
                    "errors":{
                        "lint": [...],
                        "structure": [...],
                        "vulnerability": [...]
                    }
                }
            },
            "status": "FAILED"
        }

    """
    # composing config
    echo = Echo(verbose)
    conf = dict()
    for filename in config_filenames:
        with open(filename, 'rb') as f:
            try:
                conf.update(**json.load(f))
            except ValueError:
                pass
        with open(filename, 'rb') as f:
            try:
                conf.update(**yaml.load(f, yaml.loader.SafeLoader))
            except yaml.scanner.ScannerError:
                pass

    # running tests from config
    results = dict()
    passed = True
    casenumber = 0
    for casename, caseconf in conf.items():
        casenumber += 1
        echo.info('Starting testcase {}[{}/{}]'.format(casename, casenumber, len(conf)))
        with echo.level():
            # running setup commands
            test_kwargs = caseconf['test']
            setup = caseconf['setup']
            echo.info('Starting setup')
            with echo.level():
                for setup_stage in setup:
                    env = setup_stage.get('env', {})
                    try:
                        cmd = setup_stage['cmd']
                    except KeyError:
                        echo.force_error(
                            'Setup step error in {} testcase. No "cmd" key'.format(casename)
                        )
                        raise SystemExit(2)
                    with mock.patch.dict('os.environ', env):
                        if env:
                            echo.info('Updating env...'.format(env))
                            with echo.level():
                                for key, value in env.items():
                                    echo.info('{}={}'.format(key, value), alt=True)
                        echo.info('Running cmd...')
                        with echo.level():
                            result = subprocess.run(
                                cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                            )
                            if result.returncode == 0:
                                echo.success("{}:OK!".format(cmd))
                            else:
                                echo.error("{}:FAILED!".format(cmd))
                            echo.echo((result.stdout or result.stderr).decode('utf-8'))
                echo.info('Setup completed')
            echo.info('Testing...')
            errors = test_template(**test_kwargs, verbose=verbose, _echo_level=echo._level)
            with echo.level(-1):
                echo.info('RESULT:')
                with echo.level():
                    if not errors:
                        results[casename] = dict(
                            status='PASSED',
                            errors=None
                        )
                        echo.success('PASSED!')
                    else:
                        results[casename] = dict(
                            status='FAILED',
                            errors=errors
                        )
                        passed = False
                        echo.error('FAILED!')
                    echo.info('\n')
    # selecting output method
    output = dict(results=results)
    output['status'] = "PASSED" if passed else "FAILED"
    if output_filename:
        with open(output_filename, 'wt') as f:
            json.dump(output, f, indent=4)
    if not output_filename:
        click.echo(json.dumps(output, indent=4))
    if not passed:
        raise SystemExit(1)


@root.command(
    name='test',
    short_help='perform 3 stages test of CF template file',
    context_settings=dict(
        max_content_width=120
    )
)
@click.option(
    '--file',
    'filename',
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        exists=True
    ),
    required=True,
    help='CF template filename. Accepts YAML and JSON formats'
)
@click.option(
    '--match',
    nargs=2,
    multiple=True,
    help='match <json.path> <value>. Value can be scalar, list or object'
)
@click.option(
    '--resource',
    nargs=2,
    multiple=True,
    help='resource <id> <type> exists'
)
@click.option(
    '--output',
    nargs=1,
    multiple=True,
    help='output <id> exists'
)
@click.option(
    '--length',
    type=(str, int),
    multiple=True,
    help='length <json.path> <length>. Can check str, list, object'
)
@click.option(
    '--exists',
    nargs=1,
    multiple=True,
    help='exist <json.path>. Value can be null'
)
@click.option(
    '--not-empty',
    nargs=1,
    multiple=True,
    help='not empty <json.path>. Value must have length > 0 and != null'
)
@click.option(
    '--no-lint',
    is_flag=True,
    help='disable cfn-lint check'
)
@click.option(
    '--no-vulnerability-check',
    is_flag=True,
    help='disable cfn-nag check'
)
def test_signle_template(**kwargs):
    """
    Performs 3 stage test of CF template file

    \b
    Stages:
        1. cfn-lint, results stored under "lint" key
        2. structure check, results stored under "structure" key,
        3. cfn-nag, results stored under "vulnerability" key

    \b
    NOTE:
        Stages 1 and 3 can be disabled by corresponding flags.

    \b
    Output Format:
        {
            "lint": [...],
            "structure": [...],
            "vulnerability": [...]
        }
    """
    try:
        output = test_template(**kwargs)
    except ValueError as e:
        click.echo(str(e))
        raise SystemExit(2)
    for key, value in output.items():
        if value:
            click.echo(json.dumps(output, indent=4))
            raise SystemExit(1)
    click.echo('OK')


def test_template(
    filename=None,
    # rules
    match=None,
    resource=None,
    output=None,
    length=None,
    exists=None,
    not_empty=None,
    # flags
    no_lint=False,
    no_vulnerability_check=False,
    verbose=False,
    _echo_level=0,
):
    # setting test conditions defaults
    match = match or []
    resource = resource or []
    output = output or []
    length = length or []
    exists = exists or []
    not_empty = not_empty or []

    echo = Echo(verbose)
    echo._level = _echo_level

    if not no_lint:
        echo.info('Linter check...')
        with echo.level():
            errors = find_linter_errors(filename)
            if errors:
                echo.error('FAILED')
                return dict(lint=errors)
            echo.success('PASSED')
    else:
        echo.info('Linter skipped')
    body = None
    with open(filename, 'rb') as f:
        try:
            body = json.load(f)
        except ValueError:
            pass
    with open(filename, 'rb') as f:
        try:
            body = load_yaml(f)
        except yaml.scanner.ScannerError:
            pass
    if body is None:
        raise ValueError("Can't read file {}".format(filename), err=True)

    echo.info('Structural check...')
    template = Template(body)
    with echo.level():
        for path, pattern in match:
            echo.info('match {} {}'.format(path, pattern), alt=True)
            if isinstance(pattern, str):
                try:
                    pattern = json.loads(pattern)
                except ValueError:
                    pass
            template.match(path, pattern)
        for id, type in resource:
            echo.info('resource {} {}'.format(id, type), alt=True)
            template.resource(id, type)
        for id in output:
            echo.info('output {}'.format(id), alt=True)
            template.output(id)
        for path, value in length:
            echo.info('length {} {}'.format(path, value), alt=True)
            template.len(path, value)
        for path in exists:
            echo.info('exists {}'.format(path), alt=True)
            template.exists(path)
        for path in not_empty:
            echo.info('not empty {}'.format(path), alt=True)
            template.not_empty(path)
        if template.errors:
            echo.error('FAILED')
            return dict(structure=template.errors)
        echo.success('PASSED')
    if not no_vulnerability_check:
        echo.info('Vulnerability check...')
        with echo.level():
            errors = find_potential_vulnerabilities(filename)
            if errors:
                echo.error('FAILED')
                return dict(vulnerability=errors)
            echo.success('PASSED')
    else:
        echo.info('Vulnerability check skipped')
    return dict()


root()
