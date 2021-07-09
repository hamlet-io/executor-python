from hamlet.command import root as cli

#  to avoid mock.patch path interpretation issuses
from .generate import geneate as generate_cmd
from .run import run as run_cmd


@cli.group("test", context_settings=dict(max_content_width=240))
def group():
    """
    Tests stuff
    """


group.add_command(generate_cmd)
group.add_command(run_cmd)
