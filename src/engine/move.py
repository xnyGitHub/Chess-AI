"""
Move class that holds the defferent types of moves available and info about it
Normal | Capture | Castle | EnPassant | Check | Checkmate
"""
# pylint: disable=too-few-public-methods


class Move:
    """Class that stores info about a move"""

    def __init__(self, start_square, end_square):
        """Each move has a move type Normal | Capture | Castle | EnPassant
        start_square: (tuple) -> (row,col)
        end_square: (tuple) -> (row,col)
        """
        self.start_square = start_square
        self.end_square = end_square
        self.movetype = Move.__name__
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]

    def __repr__(self) -> str:
        """Repr function for debugging and visualisation"""
        return f"""{self.start_square=}
{self.end_square=}
{self.movetype=}
"""


class Capture(Move):
    """Class responsible for piece captures"""

    def __init__(self, start_square, end_square, board):
        super().__init__(start_square, end_square)
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.movetype = Capture.__name__

    def __repr__(self) -> str:
        """Repr function for debugging and visualisation"""
        return f"""{self.start_square=}
{self.end_square=}
{self.movetype=}
{self.piece_moved=}
{self.piece_captured=}
"""
