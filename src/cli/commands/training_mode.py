"""Click interface for two player mode
User gets here by entering: chess ai [OPTIONAL] COMMANDS """
import click
from src.engine.main import run


@click.command()
def training():
    """
    Make both moves for black and white. Training
    """
    run()
    click.echo("You chose training")
