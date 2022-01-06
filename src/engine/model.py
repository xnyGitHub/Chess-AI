"""Model class part of the MVC"""
import numpy as np
from src.engine.event_manager import QuitEvent, TickEvent, ClickEvent
from src.utils.model_helpers import piece_movemovents


class GameEngine:
    """Holds the game state."""

    def __init__(self, ev_manager):
        """Create new gamestate"""

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.running = False

        self.square_selected = ()
        self.player_clicks = []
        self.most_recent_valid_move_click = []

        self.white_moves = []
        self.black_moves = []
        self.piece_moves = piece_movemovents()

        """Default board constructor"""
        self.board = np.array(
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
    def is_in_bounds(new_x, new_y):
        """Check if a set of cords is in-bounds"""
        if 0 <= new_x <= 7 and 0 <= new_y <= 7:
            return True
        return False

    def generate_all_moves(self):
        """Function that calls get moves"""
        # Clear each time otherwise we end up with duplicates
        self.white_moves.clear()
        self.black_moves.clear()

        # Loop board and get moves for each pieace
        for index, chess_square in np.ndenumerate(self.board):
            if chess_square != "--":
                movements = self.piece_moves[chess_square[1]]["movements"]
                is_continious = self.piece_moves[chess_square[1]]["continous"]
                self.generate_moves(index, chess_square, movements, is_continious)

    def generate_moves(
        self, index: tuple, chess_square: str, movements: list, is_continious: bool
    ) -> None:
        """Generate non-pawn moves here"""
        row, col = index
        piece_color, piece_type = chess_square
        array = self.white_moves if piece_color == "w" else self.black_moves

        if piece_type != "P":  # If not pawn
            for x, y in movements:  # Grab offsets
                new_row, new_col = row + x, col + y  # Get new pos
                while self.is_in_bounds(new_row, new_col):  #
                    # Check if the square is empty
                    if self.board[new_row][new_col] == "--":
                        array.append(
                            {
                                "start": (row, col),
                                "end": (new_row, new_col),
                                "type": "Normal",
                            }
                        )
                        if not is_continious:
                            break
                        new_row += x
                        new_col += y
                    else:
                        # Collides with team piece
                        if self.board[new_row][new_col][0] == piece_color:
                            break
                        # Collides with enemy piece
                        array.append(
                            {
                                "start": (row, col),
                                "end": (new_row, new_col),
                                "type": "Capture",
                            }
                        )
                        break
            return

        # Line reached only if piece is pawn
        # Set direction
        direction = -1 if piece_color == "w" else 1
        # Check if its inbounds
        if self.is_in_bounds(row + direction, col):
            if self.board[row + direction][col] == "--":  # If empty
                array.append(
                    {
                        "start": (row, col),
                        "end": (row + direction, col),
                        "type": "Normal",
                    }
                )

                # Two square move
                if (
                    (row == 6 and piece_color == "w")
                    or (row == 1 and piece_color == "b")
                    and self.board[row + (direction * 2)][col] == "--"
                ):
                    array.append(
                        {
                            "start": (row, col),
                            "end": (row + (direction * 2), col),
                            "type": "Normal",
                        }
                    )
            # Capture
            offset = [1, -1]
            for x in offset:
                if 0 <= (col + x) <= 7:
                    if self.board[row + direction][col + x][0] != "-":
                        if (
                            self.board[row + direction][col + x][0] != piece_color
                        ):  # Move up left check
                            array.append(
                                {
                                    "start": (row, col),
                                    "end": (row + direction, col + x),
                                    "type": "Capture",
                                }
                            )

    def notify(self, event):
        """Called by an event in the message queue."""

        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, ClickEvent):
            col = int(event.location[0] / 64)
            row = int(event.location[1] / 64)
            if self.square_selected == (col, row) or col >= 8 or row >= 8:
                self.square_selected = ()
                self.player_clicks = []
            else:  # Else if the user clicks on a different square we append it to player clicks
                self.square_selected = col, row
                self.player_clicks.append(self.square_selected)
                if len(self.player_clicks) == 2:
                    self.most_recent_valid_move_click = self.player_clicks
                    self.square_selected = ()
                    self.player_clicks = []

    def run(self, testing: bool = False):
        """
        Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.running = True
        if testing:
            for _ in range(3):
                new_tick = TickEvent()
                self.ev_manager.post(new_tick)
        else:
            while self.running:
                new_tick = TickEvent()
                self.ev_manager.post(new_tick)
