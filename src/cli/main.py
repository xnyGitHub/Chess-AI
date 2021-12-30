"""Main entry point for cli"""
import click
from src.cli.commands.training_mode import training_mode


@click.group()
def menu():
    """Entry point for click cli"""


menu.add_command(training_mode)
