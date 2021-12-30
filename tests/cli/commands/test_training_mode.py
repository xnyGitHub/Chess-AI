"""Unit test for src/cli/commands/training_mode.py"""
from unittest.mock import patch
from click.testing import CliRunner
from tests.cli.helpers import menu_training_mode
from src.cli.commands.training_mode import training_mode


@patch("src.cli.commands.training_mode.run")
def test_traning_mode(mock_run):
    """Test the training-mode commands for the click interface"""
    runner = CliRunner()
    result = runner.invoke(training_mode, [])
    mock_run.return_value = True
    expected_result = menu_training_mode()

    assert result.exit_code == 0
    assert result.output == expected_result
