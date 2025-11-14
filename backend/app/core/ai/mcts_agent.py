from __future__ import annotations
import math
import random
import time
from typing import Optional, Tuple, Dict
from app.core.ai.base_agent import BaseAgent
from app.core.engine.board import Board, BLACK, WHITE
from app.core.eval.evaluator import Evaluator

Move = Tuple[int, int]


class MCTSNode:
    def __init__(self, board: Board, parent: Optional["MCTSNode"],
                 move_from_parent: Optional[Move], player_just_moved: int):
        self.board_snapshot = board.copy()
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.player_just_moved = player_just_moved
        self.children: Dict[Move, MCTSNode] = {}
        self.visits = 0
        self.wins = 0.0  # wins for player_just_moved

    def is_fully_expanded(self, player_to_move: int) -> bool:
        return len(self.children) == len(self.board_snapshot.legal_moves(player_to_move))

    def uct_score(self, total_simulations: int, c: float = math.sqrt(2)):
        if self.visits == 0:
            return float("inf")
        win_rate = self.wins / self.visits
        return win_rate + c * math.sqrt(math.log(total_simulations) / self.visits)


class MCTSAgent(BaseAgent):
    def __init__(self, evaluator: Optional[Evaluator] = None,
                 simulations: int = 1000, time_limit: Optional[float] = None,
                 rollout_policy: str = "random"):
        self.evaluator = evaluator
        self.simulations = simulations
        self.time_limit = time_limit
        self.rollout_policy = rollout_policy

    def best_move(self, board: Board, player: int):
        root = MCTSNode(board.copy(), None, None, -player)
        end_time = time.time() + self.time_limit if self.time_limit else None

        sims = 0

        while True:
            if end_time and time.time() > end_time:
                break
            if self.time_limit is None and sims >= self.simulations:
                break

            sims += 1
            node = root
            state = board.copy()

            # SELECTION
            while node.children and not state.is_terminal():
                best_move, best_child = max(
                    node.children.items(),
                    key=lambda it: it[1].uct_score(node.visits)
                )
                state.apply_move(best_move, -node.player_just_moved)
                node = best_child

            # EXPANSION
            player_to_move = state.to_move
            legal = state.legal_moves(player_to_move)

            if legal and not node.is_fully_expanded(player_to_move):
                tried = set(node.children.keys())
                untried = [m for m in legal if m not in tried]
                if untried:
                    mv = random.choice(untried)
                    state.apply_move(mv, player_to_move)
                    child = MCTSNode(state.copy(), node, mv, player_to_move)
                    node.children[mv] = child
                    node = child

            # ROLLOUT
            winner = self._rollout(state)

            # BACKPROP
            self._backpropagate(node, winner)

        # --- FIXED: avoid empty children meaning 'pass' ---
        root_moves = board.legal_moves(player)

        if not root.children:
            # MCTS failed to expand → return any legal move rather than passing
            if root_moves:
                return root_moves[0], 0.0
            return None, 0.0

        # Pick move with highest visit count
        best_mv, best_child = max(root.children.items(), key=lambda it: it[1].visits)
        score = best_child.wins / best_child.visits if best_child.visits else 0.0
        return best_mv, float(score)

    def _rollout(self, state: Board) -> int:
        sim = state.copy()
        while not sim.is_terminal():
            moves = sim.legal_moves(sim.to_move)
            if not moves:
                sim.apply_move(None, sim.to_move)
                continue

            if self.rollout_policy == "random" or self.evaluator is None:
                mv = random.choice(moves)
            else:
                # greedy rollout
                best_mv = None
                best_score = float('-inf')
                for mv in moves:
                    sim.apply_move(mv, sim.to_move)
                    score = self.evaluator.evaluate(sim, BLACK)
                    sim.undo()

                    if score > best_score:
                        best_score = score
                        best_mv = mv

                mv = best_mv or random.choice(moves)

            sim.apply_move(mv, sim.to_move)

        return sim.winner()

    def _backpropagate(self, node: MCTSNode, winner: int):
        while node:
            node.visits += 1
            if winner == node.player_just_moved:
                node.wins += 1
            node = node.parent
