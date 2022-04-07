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
    "--commit-type",
    help="The type of commit to assign these changes to",
    default="cd",
    type=click.Choice(
        [
            "cd",
            "feat",
            "chore",
            "fix",
            "refactor",
        ]
    ),
)
@click.option(
    "-d",
    "--commit-description",
    default="deploy_updates",
)
@click.option(
    "-m",
    "--commit-message",
    required=True,
    help="The commit message for these changes",
)
@click.option(
    "-b",
    "--branch",
    help="The repository reference to commit changes on",
)
@click.option(
    "--tag",
    help="The name of a tag to apply to the commit",
)
@click.option("--push/--no-push", default=True, help="Push committed changes")
@exceptions.backend_handler()
@config.pass_options
def commit_changes(
    options,
    accounts,
    products,
    commit_type,
    commit_description,
    commit_message,
    branch,
    tag,
    push,
    **kwargs,
):
    """
    Commit changes made to all CMDBs to their repositories
    """

    message = [
        f"cctype={commit_type}",
        f"ccdesc={commit_description}",
        f"msg={commit_message}",
    ]

    if accounts:
        message.append(f"account={options.account}")

    if products:
        message.append(f"product={options.product}")

    command_args = {
        "account_repos": accounts,
        "product_repos": products,
        "commit_message": ", ".join(message),
        "reference": branch,
        "defer_push": not push,
        "tag": tag,
    }

    task = save_repos_backend.SaveCMDBAutomationRunner(
        **options.opts, **kwargs, **command_args, engine=options.engine
    )
    task.run()
