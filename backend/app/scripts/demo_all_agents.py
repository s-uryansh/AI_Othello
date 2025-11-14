import os
import time
from datetime import datetime
from app.core.engine.board import Board, BLACK, WHITE
from app.core.eval.evaluator import Evaluator
from app.core.ai.random_agent import RandomAgent
from app.core.ai.greedy_agent import GreedyAgent
from app.core.ai.minimax_agent import MinimaxAgent
from app.core.ai.mcts_agent import MCTSAgent
from app.core.ai.hybrid_agent import HybridAgent

LOG_DIR = "app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def print_board(b: Board) -> str:
    """Return board as printable string."""
    s = "\n   " + " ".join(str(c) for c in range(b.size)) + "\n"
    for r in range(b.size):
        row = " ".join({0: ".", 1: "B", -1: "W"}[b.grid[r][c]] for c in range(b.size))
        s += f"{r}  {row}\n"
    return s

def run_match(agent_name: str, agent):
    """Run a short AI vs AI match for demonstration."""
    b = Board()
    moves_played = 0
    log_lines = [f"=== {agent_name} Demo ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n"]
    log_lines.append(print_board(b))

    while not b.is_terminal() and moves_played < 20:  # short demo
        mv, score = agent.best_move(b, b.to_move)
        moves_played += 1
        if mv is None:
            log_lines.append(f"Move {moves_played}: {'BLACK' if b.to_move==BLACK else 'WHITE'} has no legal moves (pass)\n")
            b.apply_move(None, b.to_move)
            continue
        b.apply_move(mv, b.to_move)
        log_lines.append(f"Move {moves_played}: {'BLACK' if b.to_move==-1 else 'WHITE'} played {mv}, Eval={score:.2f}\n")
        log_lines.append(print_board(b))
        time.sleep(0.2)

    b_score, w_score = b.score()
    winner = "BLACK 🏴" if b_score > w_score else "WHITE ⚪" if w_score > b_score else "DRAW"
    log_lines.append(f"Game Over — BLACK: {b_score}, WHITE: {w_score}, Winner: {winner}\n")
    return log_lines

def main():
    ev = Evaluator()
    agents = {
        "RandomAgent": RandomAgent(seed=42),
        "GreedyAgent": GreedyAgent(ev),
        "MinimaxAgent": MinimaxAgent(ev, max_depth=3, time_limit=1.5),
        "MCTSAgent": MCTSAgent(ev, simulations=200, time_limit=1.5),
        "HybridAgent": HybridAgent(ev, use_mcts=True, deep_depth=4, time_limit=1.5),
    }

    for name, agent in agents.items():
        lines = run_match(name, agent)
        fname = f"{LOG_DIR}/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(fname, "w") as f:
            f.writelines(lines)
        print(f"[+] {name} demo complete — logged to {fname}")

if __name__ == "__main__":
    main()
