"""Test class for src/engine/board.py"""  # pylint: disable=too-few-public-methods
from unittest.mock import patch
from src.engine.model import GameEngine
from src.engine.event_manager import EventManager, ClickEvent, QuitEvent
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


class TestClickEvents:
    """Class for testing whether click events are regsitered"""

    def test_two_valid_click_events(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == (7, 7)
        assert game_engine.player_clicks == [(7, 7)]
        assert not game_engine.most_recent_valid_move_click

        click_event = ClickEvent((511, 447))
        event_manager.post(click_event)
        assert not game_engine.square_selected
        assert not game_engine.player_clicks
        assert game_engine.most_recent_valid_move_click == [(7, 7), (7, 6)]

    def test_invalid_click_event(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((800, 510))
        event_manager.post(click_event)
        assert not game_engine.square_selected
        assert not game_engine.player_clicks

    def test_two_valid_same_cord_click_events(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == (7, 7)
        assert game_engine.player_clicks == [(7, 7)]
        assert not game_engine.most_recent_valid_move_click

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert not game_engine.square_selected
        assert not game_engine.player_clicks
        assert not game_engine.most_recent_valid_move_click

    def test_valid_then_invalid_click_event(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == (7, 7)
        assert game_engine.player_clicks == [(7, 7)]
        assert not game_engine.most_recent_valid_move_click

        click_event = ClickEvent((513, 513))
        event_manager.post(click_event)
        assert not game_engine.square_selected
        assert not game_engine.player_clicks
        assert not game_engine.most_recent_valid_move_click
