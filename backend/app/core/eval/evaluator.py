from __future__ import annotations
from typing import Dict
from app.core.engine.board import Board, BLACK
from app.core.eval.features import extract_features

class Evaluator:
    def __init__(self, weights: Dict[str, float] | None = None) -> None:
        # Default weights safe starting point
        self.weights = weights or {
            "disc_diff": 1.0,
            "mobility": 5.0,
            "corner_occupancy": 25.0,
            "corner_adj": 10.0,
            "frontier": 2.0,
        }

    def evaluate(self, board: Board, player: int) -> float:
        """Compute board evaluation based on weighted feature sum."""
        feats = extract_features(board)
        score = sum(self.weights.get(k, 0.0) * v for k, v in feats.items())
        # Always return from black's perspective
        return float(score if player == BLACK else -score)
