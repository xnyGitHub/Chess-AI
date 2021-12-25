"""Main entry point for cli"""
import click


from src.cli.commands.two_player_mode import two_player
from src.cli.commands.versus_ai import ai_mode
from src.cli.commands.training_mode import training_mode
from src.cli.commands.puzzles import puzzle_mode


@click.group()
def menu():
    """Entry point for click cli"""


menu.add_command(ai_mode)
menu.add_command(two_player)
menu.add_command(training_mode)
menu.add_command(puzzle_mode)
