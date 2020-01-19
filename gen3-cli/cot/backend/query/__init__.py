import os
import json
import collections
import jmespath
from tabulate import tabulate
from jmespath.exceptions import JMESPathError
from cot.backend.create import blueprint
from cot.backend.common import context
from cot.backend.common import exceptions


def run(
    blueprint_generation_input_source=None,
    blueprint_generation_provider=None,
    blueprint_generation_framework=None,
    blueprint_generation_scenarios=None,
    blueprint_refresh=None,
    list_tiers=None,
    list_components=None,
    query=None,
    cwd=None,
    _is_cli=False
):
    ctx = context.Context(cwd)
    output_dir = os.path.join(ctx.cache, 'query', os.path.relpath(ctx.directory, ctx.root))
    blueprint_filename = os.path.join(output_dir, 'blueprint.json')
    # Due to the fact that it's hard to dermine refresh condition
    # I decided to save blueprint in the cache dir under query/cwd_cmdb_root_relpath/blueprint.json
    # This is a simplest soultuion. Logically, you create template once in certain cwd and recreate it only if
    # cache is cleared or blueprint_recreate parameter is true.

    # NOTE: Technically if we want to cache data downloaded from the remote server similar technique can be used.
    # Only thing that will change is the way to set path and cache directory
    if not os.path.exists(blueprint_filename) or blueprint_refresh:
        blueprint.run(
            generation_input_source=blueprint_generation_input_source,
            output_dir=output_dir,
            generation_provider=blueprint_generation_provider,
            generation_framework=blueprint_generation_framework,
            generation_scenarios=blueprint_generation_scenarios
        )
    with open(os.path.join(output_dir, 'blueprint.json'), 'rt') as f:
        data = json.load(f)
    result = collections.OrderedDict()
    if list_tiers:
        # TODO: extract tiers data from blueprint
        tiers = [
            {
                "Name": "DummyTierName",
                "Id": "DummyTierId",
                "NetworkEnabledState": True
            }
        ]
        result['tiers'] = tiers_table(tiers)
    if list_components:
        # TODO: extract components data from blueprint
        components = [
            {
                "Name": "DummyComponentName",
                "Id": "DummyComponentId",
                "Type": "DummyComponentType"
            }
        ]
        result['components'] = components_table(components)
    if query:
        try:
            result['query'] = jmespath.search(query, data)
        except JMESPathError as e:
            raise exceptions.UserFriendlyBackendException(f"JMESPath query error: {str(e)}") from e
    return result


def tiers_table(data):
    tablerows = []
    index = 0
    for row in data:
        index += 1
        tablerows.append([row['Name'], row['Id'], row['NetworkEnabledState']])
    return tabulate(
        tablerows,
        headers=['Name', 'Id', 'NetworkEnabledState'],
        showindex=True,
        tablefmt="psql"
    )


def components_table(data):
    tablerows = []
    index = 0
    for row in data:
        index += 1
        tablerows.append([row['Name'], row['Id'], row['Type']])
    return tabulate(
        tablerows,
        headers=['Name', 'Id', 'Type'],
        showindex=True,
        tablefmt="psql"
    )
