import click
from .PyMon import PyMon

@click.group()
def cli():
    pass

@cli.command()
@click.argument("command")
def run(command):
    pymon = PyMon(command)
    try:
        pymon.start()
    except KeyboardInterrupt:
        pymon.stop()


@cli.command()
def config():
    """for generating a global config file"""
    pass

if __name__ == "__main__":
    cli()
