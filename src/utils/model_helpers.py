"""Helper module for src/engine/model"""


def piece_movemovents():
    """Piece movement info helper function"""
    map_dict = {
        "P": {"movements": [1, -1], "continous": False},
        "R": {"movements": [(1, 0), (0, 1), (-1, 0), (0, -1)], "continous": True},
        "N": {
            "movements": [
                (-2, -1),
                (-2, 1),
                (2, -1),
                (2, 1),
                (-1, -2),
                (1, -2),
                (-1, 2),
                (1, 2),
            ],
            "continous": False,
        },
        "B": {"movements": [(1, 1), (-1, 1), (1, -1), (-1, -1)], "continous": True},
        "Q": {
            "movements": [
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
            ],
            "continous": True,
        },
        "K": {
            "movements": [
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
            ],
            "continous": False,
        },
    }
    return map_dict
