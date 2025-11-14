from __future__ import annotations
import time
import json
import os
from typing import Dict, Tuple, Type
from app.core.engine.board import Board, BLACK, WHITE
from app.core.eval.evaluator import Evaluator
from app.core.ai.random_agent import RandomAgent
from app.core.ai.greedy_agent import GreedyAgent
from app.core.ai.minimax_agent import MinimaxAgent
from app.core.ai.mcts_agent import MCTSAgent
from app.core.ai.hybrid_agent import HybridAgent

LOG_DIR = "app/logs/match_results"
os.makedirs(LOG_DIR, exist_ok=True)

AGENT_MAP: Dict[str, Type] = {
    "random": RandomAgent,
    "greedy": GreedyAgent,
    "minimax": MinimaxAgent,
    "mcts": MCTSAgent,
    "hybrid": HybridAgent,
}


class MatchRunner:
    def __init__(self, a1_name: str, a2_name: str, games: int = 10, time_limit: float = 1.5, log: bool = True):
        self.evaluator = Evaluator()
        self.a1_name = a1_name
        self.a2_name = a2_name
        self.games = games
        self.time_limit = time_limit
        self.log = log

        def _make_agent(name: str):
            cls = AGENT_MAP.get(name.lower())
            if not cls:
                raise ValueError(f"Unknown agent '{name}'")
            if name == "greedy":
                return cls(self.evaluator)
            elif name == "minimax":
                return cls(self.evaluator, max_depth=4, time_limit=self.time_limit)
            elif name == "mcts":
                return cls(self.evaluator, simulations=400, time_limit=self.time_limit)
            elif name == "hybrid":
                return cls(self.evaluator, use_mcts=True, deep_depth=4, time_limit=self.time_limit)
            else:
                return cls()

        self.agent1 = _make_agent(a1_name)
        self.agent2 = _make_agent(a2_name)

        self.results = {
            "a1": a1_name,
            "a2": a2_name,
            "games": games,
            "wins": {a1_name: 0, a2_name: 0, "draws": 0},
            "avg_move_time": {a1_name: 0.0, a2_name: 0.0},
            "avg_score_diff": 0.0,
        }

    def run(self) -> Dict:
        all_diffs = []
        for g in range(1, self.games + 1):
            b = Board()
            move_times = {self.a1_name: [], self.a2_name: []}
            log_lines = [f"\n=== Game {g}: {self.a1_name} (Black) vs {self.a2_name} (White) ===\n"]

            while not b.is_terminal():
                player = b.to_move
                agent = self.agent1 if player == BLACK else self.agent2
                agent_name = self.a1_name if player == BLACK else self.a2_name
                start_t = time.time()
                mv, _ = agent.best_move(b, player)
                elapsed = time.time() - start_t
                move_times[agent_name].append(elapsed)

                # handle passes
                if mv is None:
                    b.apply_move(None, player)
                    log_lines.append(f"{agent_name} ({'BLACK' if player == BLACK else 'WHITE'}) passes.\n")
                    continue

                # safely apply move (catch illegal ones)
                try:
                    b.apply_move(mv, player)
                    log_lines.append(
                        f"{agent_name} ({'BLACK' if player == BLACK else 'WHITE'}) plays {mv} [{elapsed:.3f}s]\n"
                    )
                except ValueError:
                    log_lines.append(f"[!] {agent_name} attempted illegal move {mv}, skipping.\n")
                    # force a pass to preserve valid game flow
                    b.apply_move(None, player)
                    continue

            # Game over — calculate results
            b_score, w_score = b.score()
            diff = b_score - w_score
            all_diffs.append(diff)

            if b_score > w_score:
                self.results["wins"][self.a1_name] += 1
                outcome = f"{self.a1_name} wins"
            elif w_score > b_score:
                self.results["wins"][self.a2_name] += 1
                outcome = f"{self.a2_name} wins"
            else:
                self.results["wins"]["draws"] += 1
                outcome = "Draw"

            avg_a1 = sum(move_times[self.a1_name]) / len(move_times[self.a1_name]) if move_times[self.a1_name] else 0
            avg_a2 = sum(move_times[self.a2_name]) / len(move_times[self.a2_name]) if move_times[self.a2_name] else 0
            self.results["avg_move_time"][self.a1_name] += avg_a1
            self.results["avg_move_time"][self.a2_name] += avg_a2

            log_lines.append(f"Final: BLACK {b_score} - WHITE {w_score}  |  {outcome}\n")

            # save per-game log
            if self.log:
                fname = f"{LOG_DIR}/match_{self.a1_name}_vs_{self.a2_name}_{g}.log"
                with open(fname, "w") as f:
                    f.writelines(log_lines)

        # Aggregate statistics
        self.results["avg_score_diff"] = sum(all_diffs) / len(all_diffs)
        self.results["avg_move_time"][self.a1_name] /= self.games
        self.results["avg_move_time"][self.a2_name] /= self.games

        # Save summary
        if self.log:
            summary_file = f"{LOG_DIR}/summary_{self.a1_name}_vs_{self.a2_name}.json"
            with open(summary_file, "w") as f:
                json.dump(self.results, f, indent=4)

        return self.results
