"""Move class where info about is move is created"""


class Move:
    """Class that stores info about a move"""

    def __init__(self, start_square, end_square, move_type):
        """Each move has a move type Normal | Capture | Castle | EnPassant"""
        self.move_type = move_type
        """start_square and end_square are stored as tuples in
        array row-col notation eg. (0,1) | (2,3)"""
        self.start_square = start_square
        self.end_square = end_square
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]

    def __repr__(self) -> str:
        """Repr function for debugging and visualisation"""
        return f"""{self.start_square=}
{self.end_square=}
{self.move_type=}
"""


class Capture(Move):
    """Class responsible for piece captures"""

    def __init__(self, start_square, end_square, move_type, board):
        super().__init__(start_square, end_square, move_type)
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def __repr__(self) -> str:
        """Repr function for debugging and visualisation"""
        return f"""{self.start_square=}
{self.end_square=}
{self.move_type=}
{self.piece_moved=}
{self.piece_captured=}
"""
