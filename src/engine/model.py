"""Model class part of the MVC"""
from typing import Union
import numpy as np

from src.engine.event_manager import (
    QuitEvent,
    TickEvent,
    ClickEvent,
    Event,
    EventManager,
)
from src.utils.model_helpers import piece_movemovents


class GameEngine:
    """Holds the game state."""

    def __init__(self, ev_manager: EventManager):
        """Create new gamestate"""

        self.ev_manager: EventManager = ev_manager
        ev_manager.register_listener(self)
        self.running: bool = False

        self.white_moves: list = []
        self.black_moves: list = []
        self.piece_moves: list = piece_movemovents()

        """Default board constructor"""
        self.board: np.array = np.array(
            [
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bB"],
            ]
        )

        self.generate_all_moves()
        for move in self.white_moves:
            print(move)

    def __repr__(self) -> str:
        """Get repr representation of the board"""
        backslash = "\n"
        return f"""GameSate(
{backslash.join(str(x) for x in self.board)}
)"""

    def __str__(self) -> str:
        """Get str representation of the board"""
        return "\n".join(" ".join(map(str, sub)) for sub in self.board)

    @staticmethod
    def is_in_bounds(new_x: int, new_y: int) -> bool:
        """Check if a set of cords is in-bounds"""
        if 0 <= new_x <= 7 and 0 <= new_y <= 7:
            return True
        return False

    @staticmethod
    def check_has_pawn_moved(current_row: int, piece_color: str) -> bool:
        """Given a row and color return whether a pawn has moved"""
        if current_row == 6 and piece_color == "w":
            return False
        if current_row == 1 and piece_color == "b":
            return False
        return True

    def get_piece_moves_dict(self, piece_type: str) -> Union[list, bool]:
        """Return info: (dict) on ghow a particular piece moves"""
        movements = self.piece_moves[piece_type]["movements"]
        continuous = self.piece_moves[piece_type]["continous"]
        return movements, continuous

    def generate_all_moves(self) -> None:
        """Function that calls get moves"""
        # Clear each time otherwise we end up with duplicates
        self.white_moves.clear()
        self.black_moves.clear()

        # Loop board and get moves for each pieace
        for index, chess_square in np.ndenumerate(self.board):
            if chess_square != "--":

                array: list = []
                piece_color: str
                piece_type: str
                piece_color, piece_type = chess_square

                if piece_color == "w":
                    array = self.white_moves
                if piece_color == "b":
                    array = self.black_moves

                if piece_type == "P":  # Pawn
                    self.get_pawn_moves(index, array, chess_square)
                else:
                    self.get_non_pawn_moves(index, array, chess_square)

    def get_non_pawn_moves(self, index: tuple, array: list, chess_square: str) -> None:
        """Generate non-pawn moves here"""
        row: int
        col: int
        row, col = index
        # ---------------
        piece_color: str
        piece_type: str
        piece_color, piece_type = chess_square
        # -------------------------------------
        movements: list
        is_continious: bool
        movements, is_continious = self.get_piece_moves_dict(piece_type)

        # Loop through piece movements list
        for add_x, add_y in movements:  # Grab offsets
            new_row, new_col = row + add_x, col + add_y  # Get new pos
            while self.is_in_bounds(new_row, new_col):  #
                # Check if the square is empty
                if self.board[new_row][new_col] == "--":
                    array.append(
                        {
                            "start_square": (row, col),
                            "end_square": (new_row, new_col),
                            "type": "Normal",
                        }
                    )
                    if not is_continious:
                        break
                    new_row += add_x
                    new_col += add_y
                else:
                    # Collides with team piece
                    if self.board[new_row][new_col][0] == piece_color:
                        break
                    # Collides with enemy piece
                    array.append(
                        {
                            "start_square": (row, col),
                            "end_square": (new_row, new_col),
                            "type": "Capture",
                        }
                    )
                    break

    def get_pawn_moves(self, index: tuple, array: list, chess_square: str) -> None:
        """Generate pawn moves"""

        # Unpack the arguments
        row: int
        col: int
        row, col = index
        # ---------------
        piece_color: str
        piece_type: str
        piece_color, piece_type = chess_square
        # -------------------------------------
        movements: list
        movements, _ = self.get_piece_moves_dict(piece_type)

        # Set pawn direction
        if piece_color == "w":
            direction = -1
        if piece_color == "b":
            direction = 1

        # Check if its inbounds
        if self.is_in_bounds(row + direction, col):
            if self.board[row + direction][col] == "--":  # If empty
                array.append(
                    {
                        "startself.white_moves": (row, col),
                        "end_square": (row + direction, col),
                        "type": "Normal",
                    }
                )

                # Two square move
                if (
                    not self.check_has_pawn_moved(row, piece_color)
                    and self.board[row + (direction * 2)][col] == "--"
                ):
                    array.append(
                        {
                            "start_square": (row, col),
                            "end_square": (row + (direction * 2), col),
                            "type": "Normal",
                        }
                    )
            # Capture
            for add_y in movements:
                if 0 <= (col + add_y) <= 7:
                    if self.board[row + direction][col + add_y][0] != "-":
                        if (
                            self.board[row + direction][col + add_y][0] != piece_color
                        ):  # Move up left check
                            array.append(
                                {
                                    "start_square": (row, col),
                                    "end_square": (row + direction, col + add_y),
                                    "type": "Capture",
                                }
                            )

    def notify(self, event: Event) -> None:
        """Called by an event in the message queue."""

        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, ClickEvent):
            print(f"recieved {event.location}")

    def run(self) -> None:
        """Starts the game engine loop. Keep running until QuitEvent()"""
        self.running = True
        while self.running:
            new_tick = TickEvent()
            self.ev_manager.post(new_tick)
