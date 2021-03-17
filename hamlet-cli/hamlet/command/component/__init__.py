from hamlet.command import root as cli

from hamlet.command.component.describe_occurrence import describe_occurrence as describe_occurrence_group
from hamlet.command.component.list_occurrences import list_occurrences as list_occurrences_command


@cli.group('component')
def component_group():
    """
    Provides information on the components used in a hamlet
    """
    pass


component_group.add_command(describe_occurrence_group)
component_group.add_command(list_occurrences_command)
