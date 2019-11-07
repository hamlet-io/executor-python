from src.command import group as cli
from .template import template
from .blueprint import blueprint


@cli.group('create')
def group():
    """
    Creates stuff
    """


group.add_command(template)
group.add_command(blueprint)
