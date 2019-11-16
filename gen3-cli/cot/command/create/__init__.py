from cot.command import root as cli
#  to avoid mock.patch path interpretation issuses
from .template import template as template_cmd
from .blueprint import blueprint as blueprint_cmd
from .build_blueprint import build_blueprint as build_blueprint_cmd
from .reference import reference as reference_cmd


@cli.group('create')
def group():
    """
    Creates stuff
    """


group.add_command(template_cmd)
group.add_command(blueprint_cmd)
group.add_command(build_blueprint_cmd)
group.add_command(reference_cmd)
