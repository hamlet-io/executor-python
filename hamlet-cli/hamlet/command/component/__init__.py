from hamlet.command import root as cli

from hamlet.command.component.describe_occurrence import describe_occurrence as describe_occurrence_group
from hamlet.command.component.list_occurrences import list_occurrences as list_occurrences_command


@cli.group('component')
def group():
    """
    Provides information on the components used in a hamlet
    """
    pass


group.add_command(describe_occurrence_group)
group.add_command(list_occurrences_command)
