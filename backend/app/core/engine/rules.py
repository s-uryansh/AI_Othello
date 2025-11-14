from typing import List, Tuple
EMPTY = 0
BLACK = 1
WHITE = -1
Move = Tuple[int, int]

DIRECTIONS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]

def get_flips(grid: List[List[int]], r: int, c: int, player: int) -> List[Move]:
    if grid[r][c] != EMPTY:
        return []
    size = len(grid)
    flips = []
    for dr, dc in DIRECTIONS:
        rr, cc = r + dr, c + dc
        line = []
        while 0 <= rr < size and 0 <= cc < size and grid[rr][cc] == -player:
            line.append((rr, cc))
            rr += dr
            cc += dc
        if 0 <= rr < size and 0 <= cc < size and grid[rr][cc] == player and line:
            flips.extend(line)
    return flips
