from hamlet.command import root as cli
#  to avoid mock.patch path interpretation issuses
from .template import template as template_cmd
from .blueprint import blueprint as blueprint_cmd
from .buildblueprint import buildblueprint as buildblueprint_cmd
from .reference import reference as reference_cmd
from .unitlist import unitlist as unitlist_cmd


@cli.group('create')
def group():
    """
    Creates stuff
    """


group.add_command(template_cmd)
group.add_command(blueprint_cmd)
group.add_command(buildblueprint_cmd)
group.add_command(reference_cmd)
group.add_command(unitlist_cmd)
