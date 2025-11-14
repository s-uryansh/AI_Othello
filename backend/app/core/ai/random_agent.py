from __future__ import annotations
import random
from typing import Optional, Tuple
from app.core.ai.base_agent import BaseAgent
from app.core.engine.board import Board

Move = Tuple[int, int]

class RandomAgent(BaseAgent):
    def __init__(self, seed: Optional[int] = None) -> None:
        if seed is not None:
            random.seed(seed)

    def best_move(self, board: Board, player: int) -> Tuple[Optional[Move], float]:
        moves = board.legal_moves(player)
        if not moves:
            return None, 0.0
        mv = random.choice(moves)
        return mv, 0.0
