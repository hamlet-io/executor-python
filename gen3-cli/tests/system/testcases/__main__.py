#!/usr/bin/env python


import json
import yaml
import click
from cfn_flip import load_yaml
from test_generic_template_structure import Template
from test_generic_template import find_potential_vulnerabilities, find_linter_errors


def output_template(lint=None, vulnerability=None, structure=None):
    return json.dumps(
        {
            'lint': lint or [],
            'structure': structure or [],
            'vulnerability': vulnerability or []
        },
        indent=4
    )


@click.command()
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
def command(
    filename,
    # rules
    match,
    resource,
    output,
    length,
    exists,
    not_empty,
    # flags
    no_lint,
    no_vulnerability_check
):
    if not no_lint:
        errors = find_linter_errors(filename)
        if errors:
            click.echo(output_template(lint=errors))
            raise SystemExit(2)
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
        click.echo("Can't read file {}".format(filename), err=True)
        raise SystemExit(1)

    template = Template(body)
    for path, pattern in match:
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
        click.echo(output_template(structure=template.errors))
        raise SystemExit(2)
    if not no_vulnerability_check:
        errors = find_potential_vulnerabilities(filename)
        if errors:
            click.echo(output_template(vulnerability=errors))
    click.echo('OK!')


command()
