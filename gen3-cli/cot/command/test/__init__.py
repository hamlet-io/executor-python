from cot.command import root as cli
#  to avoid mock.patch path interpretation issuses


@cli.group('test')
def group():
    """
    Tests stuff
    """
