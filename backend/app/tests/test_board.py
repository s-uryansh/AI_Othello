from app.core.engine.board import Board, BLACK, WHITE, EMPTY
import pytest

def test_initial_setup():
    b = Board()
    assert b.get(3,3) == WHITE
    assert b.get(4,4) == WHITE
    assert b.get(3,4) == BLACK
    assert b.get(4,3) == BLACK
    moves_black = b.legal_moves(BLACK)
    moves_white = b.legal_moves(WHITE)
    assert (2,3) in moves_black
    assert isinstance(moves_white, list)

def test_apply_and_undo():
    b = Board()
    initial = b.copy()
    moves = b.legal_moves(BLACK)
    assert moves, "Black must have initial moves"
    move = moves[0]
    b.apply_move(move, BLACK)
    assert b.get(move[0], move[1]) == BLACK
    b.undo()
    assert str(b) == str(initial)
def test_full_game_playthrough():
    b = Board()
    for _ in range(4):  # play a few valid alternating moves
        moves = b.legal_moves(b.to_move)
        assert moves, "Player should have at least one legal move"
        b.apply_move(moves[0], b.to_move)
    assert not b.is_terminal()
