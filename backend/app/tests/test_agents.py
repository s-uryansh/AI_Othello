from app.core.engine.board import Board, BLACK
from app.core.ai.random_agent import RandomAgent
from app.core.ai.greedy_agent import GreedyAgent
from app.core.ai.mcts_agent import MCTSAgent
from app.core.eval.evaluator import Evaluator

def test_agents_basic():
    b = Board()
    ev = Evaluator()
    assert RandomAgent().best_move(b, BLACK)[0] in b.legal_moves(BLACK) or RandomAgent().best_move(b,BLACK)[0] is None
    assert GreedyAgent(ev).best_move(b,BLACK)[0] in b.legal_moves(BLACK) or GreedyAgent(ev).best_move(b,BLACK)[0] is None
    mv, _ = MCTSAgent(evaluator=ev, simulations=50, time_limit=0.2).best_move(b,BLACK)
    assert mv in b.legal_moves(BLACK) or mv is None
