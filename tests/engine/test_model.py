"""Test class for src/engine/board.py"""  # pylint: disable=too-few-public-methods
from unittest.mock import patch
from src.engine.model import GameEngine
from tests.helpers.general_helpers import mock_print, unmock_print
from tests.helpers.model_helpers import (
    game_engine_repr_output,
    game_engine_str_output,
    game_engine_print_output,
)


class TestGameEngine:
    """Class for testing src/engine/board.py"""

    @patch("src.engine.event_manager.EventManager")
    def test_game_enigne_registered_as_listener(self, mock_event_manager):
        """Test that the GameEngine registers itself as a listner"""
        # Arrange

        # Act
        game_engine = GameEngine(mock_event_manager)

        # Assert
        mock_event_manager.register_listener.assert_called_once_with(game_engine)

    @patch("src.engine.event_manager.EventManager")
    def test_ganme_engine_repr(self, mock_event_manager):
        """Unit test for repr magic method of GameState class"""

        # Arrange
        game_engine = GameEngine(mock_event_manager)
        expected_result = game_engine_repr_output()

        # Act
        repr_ = game_engine.__repr__()

        # Assert
        assert repr_ == expected_result

    @patch("src.engine.event_manager.EventManager")
    def test_board_class_str(self, mock_event_manager):
        """Unit test for str magic method of GameState class"""

        # Arrange
        game_engine = GameEngine(mock_event_manager)
        expected_result = game_engine_str_output()

        # Act
        str_ = game_engine.__str__()

        # Assert
        assert str_ == expected_result

    @patch("src.engine.event_manager.EventManager")
    def test_board_class_print_output(self, mock_event_manager):
        """Unit test to test the print function to sys.stdout"""

        # Arrange
        game_engine = GameEngine(mock_event_manager)
        mocked_print_output = mock_print()
        expected_result = game_engine_print_output()

        # Act
        print(game_engine)
        unmock_print()

        # Assert
        assert mocked_print_output.getvalue() == expected_result
