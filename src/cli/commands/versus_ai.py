"""Click interface for two player mode
User gets here by entering: chess ai [OPTIONAL] COMMANDS """
import click


@click.command()
def ai_mode():
    """Play chess against an ai"""
    click.echo("You chose ai timed")
