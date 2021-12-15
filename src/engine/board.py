"""Board file that handles the everything to do with the GameState Class"""


class GameState:
    """Class that handles the GameSate instance, there should only ever be one instance"""

    # _instance = None

    # def __new__(cls):
    #     """Restrict to only one gamestate being created"""
    #     if cls._instance is None:
    #         cls._instance = super(GameState, cls).__new__(cls)
    #     return cls._instance

    def __init__(self) -> None:
        """Default board constructor"""
        self.board = [["-" for _ in range(8)] for _ in range(8)]
        white_pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        black_pieces = ["r", "n", "b", "q", "k", "b", "n", "r"]

        for column in range(8):
            self.board[0][column] = white_pieces[column]
            self.board[1][column] = "P"
            self.board[6][column] = "p"
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
