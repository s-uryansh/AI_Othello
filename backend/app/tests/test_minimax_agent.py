from app.core.ai.minimax_agent import MinimaxAgent
from app.core.eval.evaluator import Evaluator
from app.core.engine.board import Board, BLACK, WHITE
import pytest

def test_minimax_basic_move():
    b = Board()
    ev = Evaluator()
    agent = MinimaxAgent(evaluator=ev, max_depth=3, time_limit=1.0)
    mv, score = agent.best_move(b, BLACK)
    assert (mv is None) or (mv in b.legal_moves(BLACK))

def test_minimax_play_sequence():
    b = Board()
    ev = Evaluator()
    agent = MinimaxAgent(evaluator=ev, max_depth=2)
    # play 4 full plies (2 moves)
    for _ in range(2):
        mv, _ = agent.best_move(b, b.to_move)
        if mv is None:
            b.apply_move(None, b.to_move)
        else:
            assert mv in b.legal_moves(b.to_move)
            b.apply_move(mv, b.to_move)
    assert not b.is_terminal()
