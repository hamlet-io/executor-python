import click
import functools
import json
import textwrap

from tabulate import tabulate

MAX_TABLE_TEXT_CONTENT_WIDTH = 128


def wrap_text(text):
    if text is None:
        return "None"
    if isinstance(text, int):
        return text
    return "\n".join(textwrap.wrap(text, MAX_TABLE_TEXT_CONTENT_WIDTH))


def table_from_dict(data):
    '''
    creates a table of k,v pairs from a list of dicts
    '''
    tablerows = []
    for k, v in data.items():
        tablerows.append([wrap_text(k), wrap_text(v)])
    return tabulate(
        tablerows,
        headers=['Key', 'Value'],
        tablefmt="github"
    )


def json_or_table_option(tablefunc):
    def decorator(func):
        click.option(
            '--output-format',
            'output_format',
            type=click.Choice(['table', 'json'], case_sensitive=False),
            default='table',
            help='Select output format'
        )(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            output_format = kwargs['output_format'].lower()
            del kwargs['output_format']
            result = func(*args, **kwargs)
            if output_format == 'table':
                click.echo(tablefunc(result))
            elif output_format == 'json':
                click.echo(json.dumps(result, indent=4))
        return wrapper
    return decorator
