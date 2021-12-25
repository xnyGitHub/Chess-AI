"""Click interface for two player mode
User gets here by entering: chess two-player [OPTIONAL] COMMANDS """
import click


@click.group()
def two_player():
    """Play chess with two players"""


@click.command("timed-mode")
@click.option("--time", required=True, help="Choose the time per side in minute(s)")
def two_player_timed(time):
    """Play chess with a timer"""
    click.echo(f"You chose timed mode with a time limit of {time} minute(s)")


@click.command("untimed-mode")
def two_player_untimed():
    """Play chess without a timer"""
    click.echo("You chose untimed mode")


two_player.add_command(two_player_untimed)
two_player.add_command(two_player_timed)
