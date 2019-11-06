# just a quick test of click capabilities
import click


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
def hello(name):
    """
    Saying "Hello"
    """
    click.echo('Hello')


@main.command()
@click.argument('name')
def bye(name):
    """
    Saying "Bye"
    """
    click.echo('Bye')


if __name__ == '__main__':
    main()