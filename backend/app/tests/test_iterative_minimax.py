from app.core.ai.minimax_agent import MinimaxAgent
from app.core.eval.evaluator import Evaluator
from app.core.engine.board import Board, BLACK
import time

def test_iterative_minimax_returns_legal_move():
    b = Board()
    ev = Evaluator()
    agent = MinimaxAgent(evaluator=ev, max_depth=5, time_limit=0.5)
    mv, score = agent.best_move(b, BLACK)
    assert (mv is None) or (mv in b.legal_moves(BLACK))

def test_time_limit_respected():
    b = Board()
    ev = Evaluator()
    agent = MinimaxAgent(evaluator=ev, max_depth=8, time_limit=0.01)
    start = time.time()
    mv, score = agent.best_move(b, BLACK)
    elapsed = time.time() - start
    assert elapsed < 1.0  # should finish quickly (tight budget)
    assert (mv is None) or (mv in b.legal_moves(BLACK))
