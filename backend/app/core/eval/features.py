from __future__ import annotations
from typing import Dict
from app.core.engine.board import Board, BLACK, WHITE, EMPTY

def extract_features(board: Board) -> Dict[str, float]:
    """Return a dictionary of board features used for evaluation."""
    feats: Dict[str, float] = {}

    b_count, w_count = board.score()
    feats["disc_diff"] = b_count - w_count

    feats["mobility"] = len(board.legal_moves(BLACK)) - len(board.legal_moves(WHITE))

    corners = [(0,0),(0,7),(7,0),(7,7)]
    corner_score = 0
    for (r,c) in corners:
        v = board.get(r,c)
        if v == BLACK:
            corner_score += 1
        elif v == WHITE:
            corner_score -= 1
    feats["corner_occupancy"] = corner_score

    adjacents = [
        (0,1),(1,0),(1,1),
        (0,6),(1,7),(1,6),
        (6,0),(7,1),(6,1),
        (6,6),(7,6),(6,7),
    ]
    adj_penalty = 0
    for (r,c) in adjacents:
        v = board.get(r,c)
        if v == BLACK:
            adj_penalty -= 1
        elif v == WHITE:
            adj_penalty += 1
    feats["corner_adj"] = adj_penalty

    frontier_black = frontier_white = 0
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for r in range(board.size):
        for c in range(board.size):
            v = board.get(r,c)
            if v == EMPTY:
                continue
            for dr,dc in dirs:
                rr,cc = r+dr,c+dc
                if board.inside(rr,cc) and board.get(rr,cc) == EMPTY:
                    if v == BLACK:
                        frontier_black += 1
                    elif v == WHITE:
                        frontier_white += 1
                    break
    feats["frontier"] = frontier_white - frontier_black

    return feats
