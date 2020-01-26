import os
import json

import collections
import jmespath

from jmespath.exceptions import JMESPathError
from cot.backend.create import blueprint
from cot.backend.common import context
from cot.backend.common import exceptions


LIST_TIERS_QUERY = (
    'Tenants[].Products[].Environments[].Segments[].Tiers[]'
    '.{'
    'Id:Id,'
    'Name:Configuration.Name,'
    'Description:Configuration.Description,'
    'NetworkEnabledState:Configuration.Network.Enabled'
    '}'
)


LIST_COMPONENTS_QUERY = (
    'Tenants[].Products[].Environments[].Segments[].Tiers[].Components[]'
    '.{Id:Id,Name:Name,Type:Type}'
)


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
    if blueprint_generation_input_source == 'mock':
        output_dir = os.path.join(ctx.cache_dir, 'query', 'mock')
    else:
        output_dir = os.path.join(ctx.cache_dir, 'query', ctx.md5_hash())
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
        result['tiers'] = jmespath.search(LIST_TIERS_QUERY, data) or []
    if list_components:
        result['components'] = jmespath.search(LIST_COMPONENTS_QUERY, data) or []
    if query:
        try:
            result['query'] = jmespath.search(query, data)
        except JMESPathError as e:
            raise exceptions.UserFriendlyBackendException(f"JMESPath query error: {str(e)}") from e
    return result
