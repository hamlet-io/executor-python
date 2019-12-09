#!/usr/bin/env python
import subprocess
import json
import yaml
from unittest import mock
import click
from cfn_flip import load_yaml
from test_generic_template_structure import Template
from test_generic_template import find_potential_vulnerabilities, find_linter_errors


@click.group()
def root():
    pass


@root.command(
    name='run'
)
@click.option(
    '-f',
    '--file',
    'filenames',
    multiple=True,
    required=True,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        readable=True,
        exists=True
    ),
    help='testcase config file'
)
@click.option(
    '-o',
    '--output',
    'output_filename',
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True
    )
)
@click.option(
    '-v',
    '--verbose',
    is_flag=True
)
def run_testcases(filenames, output_filename, verbose):

    # composing config
    conf = dict()
    for filename in filenames:
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
    for casename, caseconf in conf.items():
        # running setup commands
        test_kwargs = caseconf['test']
        setup = caseconf['setup']
        if verbose:
            stdout, stderr = None, None
        else:
            stdout, stderr = subprocess.PIPE, subprocess.PIPE
        for setup_stage in setup:
            env = setup_stage.get('env', {})
            cmd = setup_stage['cmd']
            with mock.patch.dict('os.environ', env):
                subprocess.run(
                    cmd,
                    shell=True,
                    stdout=stdout,
                    stderr=stderr
                )
        errors = test_template(**test_kwargs)
        if not errors:
            results[casename] = dict(
                status='PASSED',
                errors=None
            )
        else:
            results[casename] = dict(
                status='FAILED',
                errors=errors
            )
            passed = False
    # selecting output method
    output = dict(results=results)
    output['status'] = "PASSED" if passed else "FAILED"
    if output_filename:
        with open(output_filename, 'wt') as f:
            json.dump(output, f, indent=4)
    if not output_filename or verbose:
        click.echo(json.dumps(output, indent=4))
    if not passed:
        raise SystemExit(1)


@root.command(
    name='test'
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
    required=True
)
@click.option(
    '--match',
    nargs=2,
    multiple=True
)
@click.option(
    '--resource',
    nargs=2,
    multiple=True
)
@click.option(
    '--output',
    nargs=1,
    multiple=True
)
@click.option(
    '--length',
    type=(str, int),
    multiple=True
)
@click.option(
    '--exists',
    nargs=1,
    multiple=True
)
@click.option(
    '--not-empty',
    nargs=1,
    multiple=True
)
@click.option(
    '--no-lint',
    is_flag=True
)
@click.option(
    '--no-vulnerability-check',
    is_flag=True
)
def test_signle_template(**kwargs):
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
    no_vulnerability_check=False
):
    # setting test conditions defaults
    match = match or []
    resource = resource or []
    output = output or []
    length = length or []
    exists = exists or []
    not_empty = not_empty or []

    if not no_lint:
        errors = find_linter_errors(filename)
        if errors:
            return dict(lint=errors)
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

    template = Template(body)
    for path, pattern in match:
        if isinstance(pattern, str):
            try:
                pattern = json.loads(pattern)
            except ValueError:
                pass
        template.match(path, pattern)
    for id, type in resource:
        template.resource(id, type)
    for id in output:
        template.output(id)
    for path, value in length:
        template.len(path, value)
    for path in exists:
        template.exists(path)
    for path in not_empty:
        template.not_empty(path)

    if template.errors:
        return dict(structure=template.errors)
    if not no_vulnerability_check:
        errors = find_potential_vulnerabilities(filename)
        if errors:
            return dict(vulnerability=errors)
    return dict()


root()
