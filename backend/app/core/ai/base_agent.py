from __future__ import annotations
from typing import Optional, Tuple
from app.core.engine.board import Board

Move = Tuple[int, int]

class BaseAgent:
    """Abstract agent interface. Implementors should be light-weight and stateless if possible."""

    def best_move(self, board: Board, player: int) -> Tuple[Optional[Move], float]:
        """
        Return (move, score). Move may be None for pass.
        Score is evaluation from BLACK perspective (float).
        """
        raise NotImplementedError
