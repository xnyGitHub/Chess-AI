import pytest

from src.engine.move import Capture, Move, Castle


def test_class_move_repr():
    start_square = (0, 0)
    end_square = (1, 1)
    move_type = "Normal"
    new_move = Move(start_square, end_square, move_type)

    expected_output = """self.start_square=(0, 0)
self.end_square=(1, 1)
self.move_type='Normal'
"""
    actual_output = new_move.__repr__()
    assert actual_output == expected_output


def test_class_move_instance_of_capture():
    start_square = (0, 0)
    end_square = (1, 1)
    move_type = "Normal"
    new_move = Move(start_square, end_square, move_type)

    expected_output = False
    result = isinstance(new_move, Capture)
    assert result == expected_output


def test_class_capture_instance_of_move():
    start_square = (0, 0)
    end_square = (1, 1)
    move_type = "Normal"
    new_move = Move(start_square, end_square, move_type)

    expected_output = True
    result = isinstance(new_move, Move)
    assert result == expected_output
