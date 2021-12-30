"""Unit tests for src.cli.main"""
from click.testing import CliRunner
from src.cli.main import menu
from tests.cli.helpers import menu_helper


def test_menu():
    """Test the main entry point for the click interface"""
    runner = CliRunner()
    result = runner.invoke(menu, [])

    expected_result = menu_helper()
    assert result.output == expected_result
