"""Test class for src/engine/move.py"""  # pylint: disable=too-few-public-methods
from src.engine.move import Move, Capture


class TestMove:
    """Test for the Move class"""

    def test_class_move_repr(self):
        """Test that __repr__ works as intended"""
        start_square = (0, 0)
        end_square = (1, 1)
        new_move = Move(start_square, end_square)

        expected_output = """self.start_square=(0, 0)
self.end_square=(1, 1)
self.movetype='Move'
"""
        actual_output = new_move.__repr__()
        assert actual_output == expected_output


class TestCapture:
    """Tests for the Capture class"""

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
