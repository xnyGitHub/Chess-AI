"""Cli helpers for testing"""


def menu_helper():
    """Console output for main menu"""
    return """Usage: menu [OPTIONS] COMMAND [ARGS]...

  Entry point for click cli

Options:
  --help  Show this message and exit.

Commands:
  training-mode  Make both moves for black and white.
"""


def menu_training_mode():
    """Console output for training mode"""
    return """You chose training
"""
