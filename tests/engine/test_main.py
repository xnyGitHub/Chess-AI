"""Tests for src/engine/main.py"""  # pylint: disable=too-few-public-methods
from unittest import mock
from src.engine.main import run


class TestMain:
    """Test main module that starts the engine"""

    @mock.patch("src.engine.view.PygameView.initialise")
    @mock.patch("src.engine.model.GameEngine.run")
    def test_main(self, mock_game_engine_run, mock_view_initialise):
        "Test the entry point to the chess engine"
        run()
        mock_view_initialise.assert_called()
        mock_game_engine_run.assert_called()
