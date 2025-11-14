from __future__ import annotations
from typing import List, Tuple

# Directions in bit shifts (for an 8x8 board)
DIRECTIONS = [1, -1, 8, -8, 9, -9, 7, -7]

MASK_LEFT = 0xfefefefefefefefe
MASK_RIGHT = 0x7f7f7f7f7f7f7f7f
MASK_ALL = 0xffffffffffffffff

class BitBoard:
    def __init__(self):
        # 64-bit integers
        # Black pieces at d5,e4 (bits 28,35)
        # White pieces at e5,d4 (bits 27,36)
        self.black = (1 << (3*8+4)) | (1 << (4*8+3))
        self.white = (1 << (3*8+3)) | (1 << (4*8+4))
        self.to_move = 1  # 1=black, -1=white

    def copy(self) -> "BitBoard":
        b = BitBoard.__new__(BitBoard)
        b.black = self.black
        b.white = self.white
        b.to_move = self.to_move
        return b

    def _shift(self, bb: int, d: int) -> int:
        if d == 1:
            return (bb << 1) & MASK_LEFT
        elif d == -1:
            return (bb >> 1) & MASK_RIGHT
        elif d == 8:
            return (bb << 8) & MASK_ALL
        elif d == -8:
            return (bb >> 8) & MASK_ALL
        elif d == 9:
            return (bb << 9) & MASK_LEFT
        elif d == -9:
            return (bb >> 9) & MASK_RIGHT
        elif d == 7:
            return (bb << 7) & MASK_RIGHT
        elif d == -7:
            return (bb >> 7) & MASK_LEFT
        return 0

    def legal_moves(self, player: int) -> int:
        own = self.black if player == 1 else self.white
        opp = self.white if player == 1 else self.black
        empty = ~(own | opp) & MASK_ALL
        moves = 0
        for d in DIRECTIONS:
            mask = self._shift(own, d) & opp
            while mask:
                mask = self._shift(mask, d) & opp
            moves |= self._shift(mask, d) & empty
        return moves  # bitmask of legal move positions

    def count(self, bb: int) -> int:
        return bin(bb).count("1")

    def score(self) -> Tuple[int,int]:
        return self.count(self.black), self.count(self.white)
