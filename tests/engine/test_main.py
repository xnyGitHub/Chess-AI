"""Tests for src/engine/main.py"""  # pylint: disable=too-few-public-methods
from unittest import mock
from src.engine.main import run


class TestMain:
    """Test main module that starts the engine"""

    @mock.patch("src.engine.main.EventManager")
    @mock.patch("src.engine.main.GameEngine")
    @mock.patch("src.engine.main.PygameView")
    @mock.patch("src.engine.main.Controller")
    def test_main(
        self, mock_controller, mock_pygame_view, mock_game_engine, mock_event_manager
    ):
        "Test the entry point to the chess engine"
        run()
        mock_event_manager.assert_called()
        mock_game_engine.assert_called()
        mock_controller.assert_called()
        mock_pygame_view.assert_called()
