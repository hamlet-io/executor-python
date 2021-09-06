import click

from hamlet.command import root as cli
from hamlet.command.common import exceptions, config

from hamlet.backend.automation_tasks import save_repos as save_repos_backend


@cli.group("cmdb", context_settings=dict(max_content_width=240))
def group():
    """
    Manage CMDBs
    """


@group.command(
    "commit-changes", short_help="", context_settings=dict(max_content_width=240)
)
@click.option(
    "--accounts/--no-accounts",
    default=False,
    help="Include account repostories in save",
)
@click.option(
    "--products/--no-products",
    default=True,
    help="Include product repositories in save",
)
@click.option(
    "--commit-message",
    required=True,
    help="The commit message for these changes",
)
@click.option(
    "--reference",
    help="The repository reference to commit changes on",
)
@click.option(
    "--tag",
    help="The name of a tag to apply to the commit",
)
@exceptions.backend_handler()
@config.pass_options
def commit_changes(opts, accounts, products, commit_message, reference, tag, **kwargs):
    """
    Commit changes made to all CMDBs to their repositories
    """

    command_args = {
        "account_repos": accounts,
        "commit_message": commit_message,
        "product_repos": products,
        "reference": reference,
        "tag": tag,
    }

    task = save_repos_backend.SaveCMDBAutomationRunner(
        **opts.opts, **kwargs, **command_args
    )
    task.run()
