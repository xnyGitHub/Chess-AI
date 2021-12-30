"""Mock helpers"""
import sys
from io import StringIO


def mock_print():
    """Mock the print command"""
    mocked_print_output = StringIO()
    sys.stdout = mocked_print_output
    return mocked_print_output


def unmock_print():
    """Unmock the print command and stderr"""
    sys.stdout = sys.__stdout__
