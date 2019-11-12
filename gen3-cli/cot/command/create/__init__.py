from cot.command import root as cli
from .template import template
from .blueprint import blueprint
from .build_blueprint import build_blueprint
from .reference import reference


@cli.group('create')
def group():
    """
    Creates stuff
    """


group.add_command(template)
group.add_command(blueprint)
group.add_command(build_blueprint)
group.add_command(reference)
