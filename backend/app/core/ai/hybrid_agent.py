from __future__ import annotations
from typing import Optional, Tuple, List
from app.core.ai.base_agent import BaseAgent
from app.core.ai.greedy_agent import GreedyAgent
from app.core.ai.minimax_agent import MinimaxAgent
from app.core.ai.mcts_agent import MCTSAgent
from app.core.eval.evaluator import Evaluator
from app.core.engine.board import Board

Move = Tuple[int,int]

class HybridAgent(BaseAgent):
    def __init__(self, evaluator: Evaluator, use_mcts: bool = False, quick_depth: int = 2, deep_depth: int = 5, time_limit: float = 2.0):
        self.greedy = GreedyAgent(evaluator)
        self.minimax = MinimaxAgent(evaluator, max_depth=deep_depth, time_limit=time_limit)
        self.mcts = MCTSAgent(evaluator, simulations=500, time_limit=time_limit) if use_mcts else None
        self.quick_depth = quick_depth

    def best_move(self, board: Board, player: int) -> Tuple[Optional[Move], float]:
        # Quick greedy pass to get candidate
        mv_g, _ = self.greedy.best_move(board, player)
        if mv_g is None:
            return None, 0.0
        # If MCTS requested, run MCTS on full state
        if self.mcts is not None:
            mv_m, score = self.mcts.best_move(board, player)
            if mv_m is not None:
                return mv_m, score
        # Otherwise use minimax focused on top K candidate moves (simple: use minimax directly)
        mv_mm, score = self.minimax.best_move(board, player)
        return mv_mm or mv_g, score
