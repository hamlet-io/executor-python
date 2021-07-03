import click
import json

from hamlet.command.common import config, exceptions
from hamlet.command.common.display import json_or_table_option, table_from_dict

from .common import query_occurrences_state, DescribeContext


DESCRIBE_OCCURRENCE_QUERY = "Occurrences[?Core.TypedRawName=={name}] | [0]"


def query_occurrence_state(ctx, query=None):
    """
    Query the state of a single occurrence
    """
    options_context = ctx.ensure_object(config.Options)
    describe_context = ctx.ensure_object(DescribeContext)

    query_result = query_occurrences_state(
        options=options_context,
        query=DESCRIBE_OCCURRENCE_QUERY,
        query_params={"name": describe_context.name},
        sub_query_text=query,
    )

    return query_result


@click.group(
    "describe-occurrence",
    short_help="",
    context_settings=dict(max_content_width=240),
    invoke_without_command=True,
)
@click.option(
    "-n", "--name", required=True, help="The name of the occurrence to describe"
)
@click.option(
    "-q",
    "--query",
    help="A JMESPath query to apply to the results",
)
@exceptions.backend_handler()
@click.pass_context
def describe_occurrence(ctx, name, query):
    """
    Describe an occurrence
    """

    describe_context = DescribeContext()
    describe_context.name = name
    ctx.obj = describe_context

    if ctx.invoked_subcommand is None:
        click.echo(json.dumps(query_occurrence_state(ctx, query), indent=4))


@describe_occurrence.command(
    "solution", short_help="", context_settings=dict(max_content_width=240)
)
@exceptions.backend_handler()
@click.pass_context
def describe_occurrence_solution(ctx):
    """
    Predefined query:
    The evaluated solution configuration for the occurrence
    """
    result = query_occurrence_state(ctx, "Configuration.Solution")
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command(
    "resources", short_help="", context_settings=dict(max_content_width=240)
)
@exceptions.backend_handler()
@click.pass_context
def describe_occurrence_resources(ctx):
    """
    Predefined query:
    The resources of the occurrence
    """
    result = query_occurrence_state(ctx, "State.Resources")
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command(
    "setting-namespaces", short_help="", context_settings=dict(max_content_width=240)
)
@exceptions.backend_handler()
@click.pass_context
def describe_occurrence_setting_namespaces(ctx):
    """
    Predefined query:
    The setting namespaces for the occurrence
    """
    result = query_occurrence_state(ctx, "Configuration.SettingNamespaces")
    click.echo(json.dumps(result, indent=4))


@describe_occurrence.command(
    "attributes", short_help="", context_settings=dict(max_content_width=240)
)
@json_or_table_option(table_from_dict)
@exceptions.backend_handler()
@click.pass_context
def describe_occurrence_attributes(ctx):
    """
    Predefined query:
    The attributes for the occurrence
    """
    result = query_occurrence_state(ctx, "State.Attributes")
    return result
