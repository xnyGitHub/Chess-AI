"""Click interface puzzle mode
User gets here by entering: chess puzzle [OPTIONAL] COMMANDS """
import click
from src.engine.main import run


@click.command()
def puzzle_mode():
    """
    Play a series of chess puzzles
    """
    run()
    click.echo("You chose training")
