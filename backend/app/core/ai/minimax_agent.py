from __future__ import annotations
import time
from typing import Optional, Tuple, Dict
from enum import Enum

from app.core.engine.board import Board, BLACK, WHITE
from app.core.eval.evaluator import Evaluator
from app.core.engine.zobrist import compute_hash


class BoundType(Enum):
    EXACT = 0
    LOWER = 1
    UPPER = 2


class TTEntry:
    def __init__(self, depth: int, value: float, bound: BoundType, best_move: Optional[Tuple[int,int]]):
        self.depth = depth
        self.value = value
        self.bound = bound
        self.best_move = best_move


class MinimaxAgent:
    def __init__(self, evaluator: Evaluator, max_depth: int = 6, time_limit: Optional[float] = None) -> None:
        self.evaluator = evaluator
        self.max_depth = max_depth
        self.time_limit = time_limit  # seconds per move
        self.start_time = 0.0
        self.nodes_searched = 0
        self.tt: Dict[int, TTEntry] = {}

    def _time_exceeded(self) -> bool:
        return self.time_limit is not None and (time.time() - self.start_time) >= self.time_limit

    def best_move(self, board: Board, player: int) -> Tuple[Optional[Tuple[int,int]], float]:
        """
        Iterative deepening with transposition table.
        Returns best_move (row,col) or None for pass, and its score.
        """
        self.start_time = time.time()
        best_overall = None
        best_score_overall = float('-inf') if player == BLACK else float('inf')

        # clear TT each move (safer) — could persist across moves if desired
        self.tt.clear()

        for depth in range(1, self.max_depth + 1):
            if self._time_exceeded():
                break
            score = None
            try:
                if player == BLACK:
                    score = self._search_root(board, depth, player, True)
                else:
                    score = self._search_root(board, depth, player, True)
            except TimeoutError:
                break

            # if root search completed, extract best move from TT if present
            h = compute_hash(board.grid, board.to_move)
            entry = self.tt.get(h)
            if entry and entry.best_move is not None:
                best_overall = entry.best_move
                best_score_overall = entry.value
            # continue deeper if time allows

        # If no best found (no legal moves), return pass score
        if best_overall is None:
            moves = board.legal_moves(player)
            if not moves:
                # evaluate final position
                final_score = self.evaluator.evaluate(board, BLACK)
                return None, final_score
            # fallback: pick first legal
            return moves[0], best_score_overall
        return best_overall, best_score_overall

    def _search_root(self, board: Board, depth: int, player: int, store_best: bool) -> float:
        # root wrapper to handle no-move case and timeouts
        moves = board.legal_moves(player)
        if not moves:
            return self._evaluate_leaf(board)
        alpha = float('-inf')
        beta = float('inf')
        best_val = float('-inf') if player == BLACK else float('inf')
        best_move = None
        for mv in moves:
            if self._time_exceeded():
                raise TimeoutError()
            board.apply_move(mv, player)
            val = self._alphabeta(board, depth-1, -player, alpha, beta)
            board.undo()
            if player == BLACK:
                if val > best_val:
                    best_val = val
                    best_move = mv
                if best_val > alpha:
                    alpha = best_val
            else:
                if val < best_val:
                    best_val = val
                    best_move = mv
                if best_val < beta:
                    beta = best_val
            # optional pruning on root not necessary beyond alpha/beta
        if store_best:
            h = compute_hash(board.grid, board.to_move)
            self.tt[h] = TTEntry(depth, best_val, BoundType.EXACT, best_move)
        return best_val

    def _alphabeta(self, board: Board, depth: int, player: int, alpha: float, beta: float) -> float:
        if self._time_exceeded():
            raise TimeoutError()
        self.nodes_searched += 1

        # terminal or leaf
        if depth == 0 or board.is_terminal():
            return self._evaluate_leaf(board)

        # TT lookup
        h = compute_hash(board.grid, board.to_move)
        entry = self.tt.get(h)
        if entry is not None and entry.depth >= depth:
            if entry.bound == BoundType.EXACT:
                return entry.value
            if entry.bound == BoundType.LOWER and entry.value > alpha:
                alpha = entry.value
            elif entry.bound == BoundType.UPPER and entry.value < beta:
                beta = entry.value
            if alpha >= beta:
                return entry.value

        moves = board.legal_moves(player)
        if not moves:
            # pass move
            val = self._alphabeta(board, depth-1, -player, alpha, beta)
            # store TT
            self.tt[h] = TTEntry(depth, val, BoundType.EXACT, None)
            return val

        if player == BLACK:
            value = float('-inf')
            best_local = None
            for mv in moves:
                board.apply_move(mv, player)
                v = self._alphabeta(board, depth-1, -player, alpha, beta)
                board.undo()
                if v > value:
                    value = v
                    best_local = mv
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    break
            # store in TT
            bound = BoundType.EXACT
            if value <= alpha:
                bound = BoundType.UPPER
            elif value >= beta:
                bound = BoundType.LOWER
            self.tt[h] = TTEntry(depth, value, bound, best_local)
            return value
        else:
            value = float('inf')
            best_local = None
            for mv in moves:
                board.apply_move(mv, player)
                v = self._alphabeta(board, depth-1, -player, alpha, beta)
                board.undo()
                if v < value:
                    value = v
                    best_local = mv
                if value < beta:
                    beta = value
                if alpha >= beta:
                    break
            bound = BoundType.EXACT
            if value <= alpha:
                bound = BoundType.UPPER
            elif value >= beta:
                bound = BoundType.LOWER
            self.tt[h] = TTEntry(depth, value, bound, best_local)
            return value

    def _evaluate_leaf(self, board: Board) -> float:
        """
        Return evaluation from BLACK perspective. This is used at leaves and
        when timeouts occur (we prefer raising and catching timeout earlier).
        """
        return float(self.evaluator.evaluate(board, BLACK))
