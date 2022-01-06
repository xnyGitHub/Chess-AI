"""Model helpers for tests/engine/test_model.py"""


def game_engine_repr_output():
    """Expected GameEngine__repr__() output"""
    return """GameSate(
['wR' 'wN' 'wB' 'wQ' 'wK' 'wB' 'wN' 'wR']
['wP' 'wP' 'wP' 'wP' 'wP' 'wP' 'wP' 'wP']
['--' '--' '--' '--' '--' '--' '--' '--']
['--' '--' '--' '--' '--' '--' '--' '--']
['--' '--' '--' '--' '--' '--' '--' '--']
['--' '--' '--' '--' '--' '--' '--' '--']
['bP' 'bP' 'bP' 'bP' 'bP' 'bP' 'bP' 'bP']
['bR' 'bN' 'bB' 'bQ' 'bK' 'bB' 'bN' 'bB']
)"""


def game_engine_str_output():
    """Expected GameEngine__str__() output"""
    return """wR wN wB wQ wK wB wN wR
wP wP wP wP wP wP wP wP
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
bP bP bP bP bP bP bP bP
bR bN bB bQ bK bB bN bB"""


def game_engine_print_output():
    """Expected print(GameEngine) output"""
    return """wR wN wB wQ wK wB wN wR
wP wP wP wP wP wP wP wP
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
-- -- -- -- -- -- -- --
bP bP bP bP bP bP bP bP
bR bN bB bQ bK bB bN bB
"""
