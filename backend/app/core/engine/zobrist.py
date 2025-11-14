from __future__ import annotations
import random
from typing import List

# Deterministic seed for reproducibility
SEED = 0xC0FFEE
random.seed(SEED)

ZOBRIST_TABLE: List[List[List[int]]] = [
    [ [random.getrandbits(64) for _ in range(2)] for _ in range(8) ]
    for _ in range(8)
]
# side to move random value
ZOBRIST_SIDE = random.getrandbits(64)


def compute_hash(grid: list[list[int]], to_move: int) -> int:
    """
    Compute Zobrist hash for an 8x8 grid and side to move.
    grid values: 1 for BLACK, -1 for WHITE, 0 empty.
    """
    h = 0
    for r in range(8):
        for c in range(8):
            v = grid[r][c]
            if v == 1:
                h ^= ZOBRIST_TABLE[r][c][0]
            elif v == -1:
                h ^= ZOBRIST_TABLE[r][c][1]
    if to_move == -1:
        h ^= ZOBRIST_SIDE
    return h
