from __future__ import annotations
from typing import Optional, Tuple
from app.core.ai.base_agent import BaseAgent
from app.core.engine.board import Board
from app.core.eval.evaluator import Evaluator

Move = Tuple[int, int]

class GreedyAgent(BaseAgent):
    def __init__(self, evaluator: Evaluator) -> None:
        self.evaluator = evaluator

    def best_move(self, board: Board, player: int) -> Tuple[Optional[Move], float]:
        moves = board.legal_moves(player)
        if not moves:
            return None, self.evaluator.evaluate(board, player)
        best_mv = None
        best_score = float('-inf') if player == 1 else float('inf')
        for mv in moves:
            board.apply_move(mv, player)
            score = self.evaluator.evaluate(board, 1)  # eval from BLACK perspective
            board.undo()
            if player == 1:
                if score > best_score:
                    best_score = score; best_mv = mv
            else:
                if score < best_score:
                    best_score = score; best_mv = mv
        return best_mv, best_score
