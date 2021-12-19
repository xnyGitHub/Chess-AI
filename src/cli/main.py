"""Main entry point for cli"""
import click


from src.cli.two_player_mode import two_player
from src.cli.versus_ai import ai_mode


@click.group()
def menu():
    """Entry point for click cli"""


menu.add_command(ai_mode)
menu.add_command(two_player)
