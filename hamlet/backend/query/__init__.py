import os
import json
import tempfile

import jmespath

from jmespath.exceptions import JMESPathError
from hamlet.backend.create import template
from hamlet.backend.common import context
from hamlet.backend.common import exceptions


def run(
    cwd,
    deployment_mode=None,
    generation_entrance=None,
    generation_input_source=None,
    generation_provider=None,
    generation_framework=None,
    output_filename=None,
    use_cache=None,
    query_text=None,
    query_name=None,
    query_params=None,
    sub_query_text=None,
    log_level=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
    **kwargs,
):
    query = Query(
        cwd,
        deployment_mode=deployment_mode,
        generation_entrance=generation_entrance,
        generation_input_source=generation_input_source,
        generation_provider=generation_provider,
        generation_framework=generation_framework,
        output_filename=output_filename,
        use_cache=use_cache,
        log_level=log_level,
        root_dir=root_dir,
        tenant=tenant,
        account=account,
        product=product,
        environment=environment,
        segment=segment,
    )
    if query_name is not None:
        result = query.query_by_name(query_name, query_params or {})
    elif query_text is not None:
        result = query.query(query_text, query_params or {})
    else:
        raise exceptions.BackendException("Query unspecified")
    if sub_query_text is not None:
        result = query.perform_query(sub_query_text, result)
    return result


def mark_query(func):
    func.query_mark = True
    return func


class Query:
    LIST_TIERS_QUERY = (
        "Tenants[].Products[].Environments[].Segments[].Tiers[]"
        ".{"
        "Id:Id,"
        "Name:Configuration.Name,"
        "Description:Configuration.Description,"
        "NetworkEnabledState:Configuration.Network.Enabled"
        "}"
    )

    LIST_COMPONENTS_QUERY = (
        "Tenants[].Products[].Environments[].Segments[].Tiers[]"
        ".{"
        "TierId:Id,"
        "Components:Components[].{Id: Id, Name:Name, Type:Type}"
        "}"
    )

    LIST_OCCURRENCES_QUERY = (
        "Tenants[].Products[].Environments[].Segments[]"
        ".Tiers[?Id=={tier_id}][]"
        ".Components[?Id=={component_id}][]"
        ".Occurrences[]"
        ".{{"
        "InstanceId:Core.Instance.RawId,"
        "VersionId:Core.Version.RawId,"
        "FullName:Core.FullName,"
        "DeploymentUnits:Configuration.Solution.DeploymentUnits,"
        "Enabled:Configuration.Solution.Enabled"
        "}}"
    )

    DESCRIBE_OCCURRENCE_QUERY = (
        "Tenants[].Products[].Environments[].Segments[]"
        ".Tiers[?Id=={tier_id}][]"
        ".Components[?Id=={component_id}][]"
        ".Occurrences[?Core.Instance.RawId=={instance_id} && Core.Version.RawId=={version_id}][]"
    )

    DESCRIBE_OCCURRENCE_ATTRIBUTES_QUERY = (
        "Tenants[].Products[].Environments[].Segments[]"
        ".Tiers[?Id=={tier_id}][]"
        ".Components[?Id=={component_id}][]"
        ".Occurrences[?Core.Instance.RawId=={instance_id} && Core.Version.RawId=={version_id}][]"
        ".State.ResourceGroups.*[].Attributes[]"
    )

    DESCRIBE_OCCURRENCE_SOLUTION_QUERY = (
        "Tenants[].Products[].Environments[].Segments[]"
        ".Tiers[?Id=={tier_id}][]"
        ".Components[?Id=={component_id}][]"
        ".Occurrences[?Core.Instance.RawId=={instance_id} && Core.Version.RawId=={version_id}][]"
        ".Configuration.Solution"
    )

    DESCRIBE_OCCURRENCE_SETTINGS_QUERY = (
        "Tenants[].Products[].Environments[].Segments[]"
        ".Tiers[?Id=={tier_id}][]"
        ".Components[?Id=={component_id}][]"
        ".Occurrences[?Core.Instance.RawId=={instance_id} && Core.Version.RawId=={version_id}][]"
        ".Configuration.Settings"
    )

    DESCRIBE_OCCURRENCE_RESOURCES_QUERY = (
        "Tenants[].Products[].Environments[].Segments[]"
        ".Tiers[?Id=={tier_id}][]"
        ".Components[?Id=={component_id}][]"
        ".Occurrences[?Core.Instance.RawId=={instance_id} && Core.Version.RawId=={version_id}][]"
        ".State.Resources"
    )

    def __init__(
        self,
        cwd,
        deployment_mode,
        generation_entrance=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        output_filename=None,
        use_cache=None,
        log_level=None,
        root_dir=None,
        tenant=None,
        account=None,
        product=None,
        environment=None,
        segment=None,
    ):
        # mocked blueprint doesn't need the valid context
        if generation_input_source == "mock":
            # using static temp dir to make cache work
            tempdir = tempfile.gettempdir()
            output_dir = os.path.join(tempdir, "hamlet", "query", "mock")
        else:
            ctx = context.Context(directory=cwd, root_dir=root_dir)
            output_dir = os.path.join(ctx.cache_dir, "query", ctx.md5_hash())
        output_filepath = os.path.join(output_dir, output_filename)
        if not os.path.isfile(output_filepath) or not use_cache:
            template.run(
                output_dir=output_dir,
                deployment_mode=deployment_mode,
                entrance=generation_entrance,
                generation_input_source=generation_input_source,
                generation_provider=generation_provider,
                generation_framework=generation_framework,
                log_level=log_level,
                root_dir=root_dir,
                tenant=tenant,
                account=account,
                product=product,
                environment=environment,
                segment=segment,
            )
        with open(output_filepath, "rt") as f:
            self.blueprint_data = json.load(f)

    @mark_query
    def list_tiers(self, **params):
        return self.query(self.LIST_TIERS_QUERY)

    @mark_query
    def list_components(self, **params):
        raw_result = self.query(self.LIST_COMPONENTS_QUERY)
        result = []
        for item in raw_result:
            components = item["Components"]
            for component in components:
                result.append({**component, "TierId": item["TierId"]})
        return result

    @mark_query
    def list_occurrences(self, **params):
        return self.query(
            self.LIST_OCCURRENCES_QUERY,
            params=params,
            require=["tier_id", "component_id"],
        )

    @mark_query
    def describe_occurrence(self, **params):
        return self.query(
            self.DESCRIBE_OCCURRENCE_QUERY,
            params=params,
            require=["tier_id", "component_id", "instance_id", "version_id"],
        )

    @mark_query
    def describe_occurrence_attributes(self, **params):
        raw_result = self.query(
            self.DESCRIBE_OCCURRENCE_ATTRIBUTES_QUERY,
            params=params,
            require=["tier_id", "component_id", "instance_id", "version_id"],
        )
        result = []
        for obj in raw_result:
            for key, value in obj.items():
                result.append({"Key": key, "Value": value})
        return result

    @mark_query
    def describe_occurrence_solution(self, **params):
        return self.query(
            self.DESCRIBE_OCCURRENCE_SOLUTION_QUERY,
            params=params,
            require=["tier_id", "component_id", "instance_id", "version_id"],
        )

    @mark_query
    def describe_occurrence_settings(self, **params):
        return self.query(
            self.DESCRIBE_OCCURRENCE_SETTINGS_QUERY,
            params=params,
            require=["tier_id", "component_id", "instance_id", "version_id"],
        )

    @mark_query
    def describe_occurrence_resources(self, **params):
        return self.query(
            self.DESCRIBE_OCCURRENCE_RESOURCES_QUERY,
            params=params,
            require=["tier_id", "component_id", "instance_id", "version_id"],
        )

    def query(self, query, params=None, require=None):
        require = require or []
        params = params or {}
        if require:
            for key in require:
                try:
                    params[key]
                except KeyError as e:
                    raise exceptions.BackendException(
                        f'Missing required query param:"{key}".'
                    ) from e
        if params:
            # jsonify every param
            for key, value in params.items():
                jsonified_value = json.dumps(value)
                # need to replace double quotes with single quotes because jq is a really weird
                # and works correctly only with single quotes
                if jsonified_value.startswith('"') and jsonified_value.endswith('"'):
                    jsonified_value = f"'{jsonified_value[1:-1]}'"
                params[key] = jsonified_value
            query = query.format(**params)

        return self.perform_query(query, self.blueprint_data)

    def perform_query(self, query, data):
        if not query:
            raise exceptions.BackendException("Query can not be empty")
        try:
            return jmespath.search(query, data)
        except JMESPathError as e:
            raise exceptions.BackendException(f"JMESPath query error: {str(e)}") from e

    def query_by_name(self, name, params):
        try:
            query = getattr(self, name)
            query.query_mark
            return query(**params)
        except AttributeError:
            raise exceptions.BackendException(f'Query:"{name}" does not exist')
