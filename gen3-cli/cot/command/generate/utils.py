import click
from tabulate import tabulate


def confirm(
    kwargs,
    **confirm_kwargs
):
    confirm_kwargs['text'] = confirm_kwargs.get('text') or 'Is everything correct?'
    lines = []
    i = 1
    for key, value in kwargs.items():
        if value is None:
            continue
        name = key.replace('_', ' ')
        lines.append([i, name, value])
        i += 1
    click.echo(
        tabulate(
            lines,
            ['№', 'parameter', 'value'],
            tablefmt='psql'
        )
    )
    return click.confirm(**confirm_kwargs)
