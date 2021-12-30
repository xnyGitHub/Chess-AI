"""Test class for src/engine/board.py"""
from unittest.mock import Mock, patch
from src.engine.model import GameEngine, Move, Capture
from src.engine.event_manager import EventManager, ClickEvent
from tests.helpers.general_helpers import mock_print, unmock_print


class TestBoardState:
    """Class for testing src/engine/board.py"""

    def test_board_class_repr(self):
        """Unit test for repr magic method of GameState class"""

        # Arrange
        mock_event_manager = Mock(EventManager)
        game_engine = GameEngine(mock_event_manager)
        expected_result = """GameSate(
['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP']
['--', '--', '--', '--', '--', '--', '--', '--']
['--', '--', '--', '--', '--', '--', '--', '--']
['--', '--', '--', '--', '--', '--', '--', '--']
['--', '--', '--', '--', '--', '--', '--', '--']
['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']
['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bB']
)"""

        # Act
        repr_ = game_engine.__repr__()

        # Assert
        assert repr_ == expected_result

    def test_board_class_str(self):
        """Unit test for str magic method of GameState class"""

        # Arrange
        mock_event_manager = Mock(EventManager)
        game_engine = GameEngine(mock_event_manager)
        expected_result = """wR wN wB wQ wK wB wN wR
wP wP wP wP wP wP wP wP
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
bP bP bP bP bP bP bP bP
bR bN bB bQ bK bB bN bB"""

        # Act
        str_ = game_engine.__str__()

        # Assert
        assert str_ == expected_result

    def test_board_class_print_output(self):
        """Unit test to test the print function to sys.stdout"""

        # Arrange
        mock_event_manager = Mock(EventManager)
        game_engine = GameEngine(mock_event_manager)
        mocked_print_output = mock_print()
        expected_result = """wR wN wB wQ wK wB wN wR
wP wP wP wP wP wP wP wP
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
bP bP bP bP bP bP bP bP
bR bN bB bQ bK bB bN bB
"""

        # Act
        print(game_engine)
        unmock_print()

        # Assert
        assert mocked_print_output.getvalue() == expected_result


class TestGameEngineRunningAndQuitEvent:
    """Class for testing the game engine"""

    @patch("src.engine.event_manager.EventManager.post")
    def test_game_engine_running(self, mock_post):
        """Test game engine posts events when created"""
        # Arrange
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        # Act
        game_engine.run(True)

        # Assert
        assert game_engine.running
        assert mock_post.call_count == 3


class TestClickEvents:
    """Class for testing whether click events are regsitered"""

    def test_valid_click_event(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == (7, 7)
        assert game_engine.player_clicks == [(7, 7)]
        assert game_engine.most_recent_valid_move_click == []

        click_event = ClickEvent((511, 447))
        event_manager.post(click_event)
        assert game_engine.square_selected == ()
        assert game_engine.player_clicks == []
        assert game_engine.most_recent_valid_move_click == [(7, 7), (7, 6)]

    def test_invalid_click_event(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((800, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == ()
        assert game_engine.player_clicks == []

    def test_two_valid_click_events(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == (7, 7)
        assert game_engine.player_clicks == [(7, 7)]
        assert game_engine.most_recent_valid_move_click == []

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == ()
        assert game_engine.player_clicks == []
        assert game_engine.most_recent_valid_move_click == []

    def test_two_valid_then_invalid_events(self):
        """Unit test click_event for model.py"""
        event_manager = EventManager()
        game_engine = GameEngine(event_manager)

        click_event = ClickEvent((510, 510))
        event_manager.post(click_event)
        assert game_engine.square_selected == (7, 7)
        assert game_engine.player_clicks == [(7, 7)]
        assert game_engine.most_recent_valid_move_click == []

        click_event = ClickEvent((513, 513))
        event_manager.post(click_event)
        assert game_engine.square_selected == ()
        assert game_engine.player_clicks == []
        assert game_engine.most_recent_valid_move_click == []


class TestMove:
    """Test class for testing Moves"""

    def test_class_move_repr(self):
        """Test that __repr__ works as intended"""
        start_square = (0, 0)
        end_square = (1, 1)
        move_type = "Normal"
        new_move = Move(start_square, end_square)

        expected_output = """self.start_square=(0, 0)
self.end_square=(1, 1)
self.movetype='Move'
"""
        actual_output = new_move.__repr__()
        assert actual_output == expected_output

    def test_class_move_instance_of_capture(self):
        """Test that capture class inherits move class works as intended"""
        start_square = (0, 0)
        end_square = (1, 1)
        new_move = Move(start_square, end_square)

        expected_output = False
        result = isinstance(new_move, Capture)
        assert result == expected_output

    def test_class_capture_instance_of_move(self):
        """Test that capture class is NOT an instance of move class"""
        board = [["--" for _ in range(8)] for _ in range(8)]
        white_pieces = ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        black_pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bB"]

        for column in range(8):
            board[0][column] = white_pieces[column]
            board[1][column] = "wP"
            board[6][column] = "bP"
            board[7][column] = black_pieces[column]

        board[6][0] = "--"

        start_square = (7, 0)
        end_square = (1, 0)
        new_move = Capture(start_square, end_square, board)

        expected_output = """self.start_square=(7, 0)
self.end_square=(1, 0)
self.movetype='Capture'
self.piece_moved='bR'
self.piece_captured='wP'
"""
        assert new_move.__repr__() == expected_output
