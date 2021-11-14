from hamlet.command import root as cli

from hamlet.command.component.describe_occurrence import (
    describe_occurrence as describe_occurrence_group,
)
from hamlet.command.component.list_occurrences import (
    list_occurrences as list_occurrences_command,
)
from hamlet.command.component.query_occurrences import (
    query_occurrences as query_occurrences_command,
)
from hamlet.command.component.component_types import (
    list_component_types as list_component_types_command,
    describe_component_type as describe_component_type_command,
    query_component_types as query_component_types_command,
)


@cli.group("component", context_settings=dict(max_content_width=240))
def component_group():
    """
    Provides information on the components used in a hamlet
    """
    pass


component_group.add_command(describe_occurrence_group)
component_group.add_command(list_occurrences_command)
component_group.add_command(query_occurrences_command)
component_group.add_command(list_component_types_command)
component_group.add_command(describe_component_type_command)
component_group.add_command(query_component_types_command)
