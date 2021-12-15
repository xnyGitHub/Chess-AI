"""Utility functions for the engine"""


def get_fen_notation_from_board():
    """Create and return fen notation of current self.board"""
    return True


def get_board_from_fen_notation():
    """Create and return fen notation of current self.board"""
    return True


def convert_index_to_fen(row, col):
    """Given a row and a col, return the file and rank"""
    col_to_file = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    row_to_rank = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    file = col_to_file[col]
    rank = row_to_rank[row]
    return rank, file


def is_in_bounds(new_x, new_y):
    """Given a row and col, return True if its in-bounds"""
    if 0 <= new_x <= 7 and 0 <= new_y <= 7:
        return True
    return False


def move_log(move):
    """Function that turns move_log into fen notation"""
    start_rank, start_file = convert_index_to_fen(move.start_row, move.start_col)
    end_rank, end_file = convert_index_to_fen(move.end_row[0], move.end_col)
    piece_symbol = move.piece_moved[1] if move.piece_moved[1] != "P" else ""
    move_text = f"""{piece_symbol}
    {start_file}
    {start_rank}
    {NOTATIONS['Capture']}
    {end_file}
    {end_rank}
    {NOTATIONS[move.moveType]}"""

    return move_text

    # move_text = (
    #     str(piece_symbol)
    #     + str(start_file)
    #     + str(start_rank)
    #     + NOTATIONS["Capture"]
    #     + str(end_file)
    #     + str(end_rank)
    #     + NOTATIONS[str(piece.moveType)],
    #     True,
    #     pygame.Color("Black"),
    # )
