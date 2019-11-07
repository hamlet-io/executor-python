# just a quick test of click capabilities
import click


@click.group()
def root():
    pass


@root.command()
@click.argument('name')
def hello(name):
    """
    Saying "Hello"
    """
    click.echo('Hello')


@root.command()
@click.argument('name')
def bye(name):
    """
    Saying "Bye"
    """
    click.echo('Bye')


if __name__ == '__main__':
    root()
