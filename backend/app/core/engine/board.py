from __future__ import annotations
from typing import List, Tuple, Optional

EMPTY = 0
BLACK = 1
WHITE = -1

Move = Tuple[int, int]  # (row, col), 0-indexed

class Board:
    def __init__(self) -> None:
        self.size = 8
        self.grid: List[List[int]] = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        mid = self.size // 2
        self.grid[mid-1][mid-1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid-1][mid] = BLACK
        self.grid[mid][mid-1] = BLACK
        self.to_move = BLACK
        self.history: List[Tuple[Optional[Move], List[Move]]] = []

    def copy(self) -> "Board":
        b = Board.__new__(Board)
        b.size = self.size
        b.grid = [row[:] for row in self.grid]
        b.to_move = self.to_move
        b.history = [ (m, flips[:]) for (m, flips) in self.history ]
        return b

    def inside(self, r: int, c: int) -> bool:
        return 0 <= r < self.size and 0 <= c < self.size

    def get(self, r: int, c: int) -> int:
        return self.grid[r][c]

    def set(self, r: int, c: int, v: int) -> None:
        self.grid[r][c] = v

    def legal_moves(self, player: int) -> List[Move]:
        from .rules import get_flips
        moves: List[Move] = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != EMPTY:
                    continue
                flips = get_flips(self.grid, r, c, player)
                if flips:
                    moves.append((r, c))
        return moves

    def apply_move(self, move: Optional[Move], player: int) -> None:
        if move is None:
            self.history.append((None, []))
            self.to_move = -player
            return
        r, c = move
        from .rules import get_flips
        flips = get_flips(self.grid, r, c, player)
        if not flips:
            raise ValueError("Illegal move")
        self.set(r, c, player)
        for (fr, fc) in flips:
            self.set(fr, fc, player)
        self.history.append((move, flips))
        self.to_move = -player

    def undo(self) -> None:
        if not self.history:
            raise RuntimeError("No moves to undo")
        move, flips = self.history.pop()
        self.to_move = -self.to_move
        if move is None:
            return
        r, c = move
        self.set(r, c, EMPTY)
        for fr, fc in flips:
            self.set(fr, fc, -self.to_move)

    def is_terminal(self) -> bool:
        if self.legal_moves(BLACK) or self.legal_moves(WHITE):
            return False
        return True

    def score(self) -> Tuple[int, int]:
        black = sum(1 for r in range(self.size) for c in range(self.size) if self.grid[r][c] == BLACK)
        white = sum(1 for r in range(self.size) for c in range(self.size) if self.grid[r][c] == WHITE)
        return black, white

    def winner(self) -> int:
        b, w = self.score()
        if b > w:
            return BLACK
        if w > b:
            return WHITE
        return 0  # draw

    def __str__(self) -> str:
        rows = []
        for r in range(self.size):
            rows.append(''.join({EMPTY:'.', BLACK:'B', WHITE:'W'}[self.grid[r][c]] for c in range(self.size)))
        return "\n".join(rows)
