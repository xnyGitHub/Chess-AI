"""Model class part of the MVC"""
from src.engine.event_manager import QuitEvent, TickEvent, ClickEvent


class GameEngine:
    """Holds the game state."""

    # _instance = None

    # def __new__(cls):
    #     """Restrict to only one gamestate being created"""
    #     if cls._instance is None:
    #         cls._instance = super(GameState, cls).__new__(cls)
    #     return cls._instance

    def __init__(self, ev_manager):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        square_selected (tuple): Holds the most recent square clicked
        player_clicks (array containing tuples): Holds up to TWO tuples
        board (array): Holds the gamestate in an array
        """

        self.ev_manager = ev_manager
        ev_manager.register_listener(self)
        self.running = False
        self.square_selected = ()
        self.player_clicks = []
        self.most_recent_valid_move_click = []

        """Default board constructor"""
        self.board = [["--" for _ in range(8)] for _ in range(8)]
        white_pieces = ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        black_pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bB"]

        for column in range(8):
            self.board[0][column] = white_pieces[column]
            self.board[1][column] = "wP"
            self.board[6][column] = "bP"
            self.board[7][column] = black_pieces[column]

    def __repr__(self) -> str:
        """Get repr representation of the board"""
        backslash = "\n"
        return f"""GameSate(
{backslash.join(str(x) for x in self.board)}
)"""

    def __str__(self) -> str:
        """Get repr representation of the board"""
        return "\n".join(" ".join(map(str, sub)) for sub in self.board)

    @classmethod
    def create_gamestate_from_fen(cls, fen_string):
        """Create a gamestate from fen-notation"""

    @classmethod
    def create_gamestate_from_array(cls, fen_string):
        """Create a gamestate from a 2d-array"""

    # @property
    # def set_instance(instance):
    #     """Reset the global core"""
    #     GameState._instance = instance
    #     return GameState._instance

    # @property
    # def reset_instance():
    #     """Reset the global core"""
    #     GameState._instance = None

    # @property
    # def get_instance():
    #     """Get the board in fen-notation"""
    #     if GameState._instance is None:
    #         GameState._instance = GameState()
    #     return GameState._instance

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
        self.board = board
        self.movetype = Capture.__name__

    def __repr__(self) -> str:
        """Repr function for debugging and visualisation"""
        return f"""{self.start_square=}
{self.end_square=}
{self.movetype=}
{self.piece_moved=}
{self.piece_captured=}
"""
