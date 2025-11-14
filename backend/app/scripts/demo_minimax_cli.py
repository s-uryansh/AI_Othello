from app.core.engine.board import Board, BLACK, WHITE
from app.core.ai.minimax_agent import MinimaxAgent
from app.core.eval.evaluator import Evaluator
import time

def print_board(b: Board):
    print("\n   " + " ".join(str(c) for c in range(b.size)))
    for r in range(b.size):
        row = " ".join({0: ".", 1: "B", -1: "W"}[b.grid[r][c]] for c in range(b.size))
        print(f"{r}  {row}")
    print()

def run_demo():
    b = Board()
    ev = Evaluator()
    black_ai = MinimaxAgent(ev, max_depth=3, time_limit=1.0)
    white_ai = MinimaxAgent(ev, max_depth=3, time_limit=1.0)

    print("Initial Board:")
    print_board(b)
    time.sleep(1)

    move_count = 0
    while not b.is_terminal():
        player = b.to_move
        agent = black_ai if player == BLACK else white_ai
        mv, score = agent.best_move(b, player)
        move_count += 1

        if mv is None:
            print(f"{'BLACK' if player==BLACK else 'WHITE'} has no legal move. Passing turn.\n")
            b.apply_move(None, player)
            continue

        b.apply_move(mv, player)
        print(f"Move {move_count}: {'BLACK' if player==BLACK else 'WHITE'} plays {mv}, Eval={score:.2f}")
        print_board(b)
        time.sleep(0.7)

        if move_count > 60:
            break  # safety cutoff

    b_score, w_score = b.score()
    print("\nGame Over!")
    print(f"Final Score -> BLACK: {b_score}, WHITE: {w_score}")
    if b_score > w_score:
        print("Winner: BLACK 🏴")
    elif w_score > b_score:
        print("Winner: WHITE ⚪")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    run_demo()
