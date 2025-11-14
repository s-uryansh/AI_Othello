from __future__ import annotations
import json
import os
import matplotlib.pyplot as plt

VALIDATION_LOG = "app/logs/validation/validation_summary.json"
OUTPUT_DIR = "app/logs/validation/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_results():
    if not os.path.exists(VALIDATION_LOG):
        raise FileNotFoundError(f"Missing {VALIDATION_LOG}")
    with open(VALIDATION_LOG, "r") as f:
        data = json.load(f)
    return data

def analyze():
    print("\n=== ANALYZING VALIDATION RESULTS ===")
    data = load_results()

    opponents = []
    win_rates = []
    avg_diffs = []

    for opp, result in data.items():
        w = result["wins"]["minimax"]
        g = result["games"]
        wr = (w / g) * 100 if g else 0
        opponents.append(opp.upper())
        win_rates.append(wr)
        avg_diffs.append(result["avg_score_diff"])

    # Plot 1: Win rates
    plt.figure(figsize=(6, 4))
    plt.bar(opponents, win_rates)
    plt.title("Trained Agent Win Rate vs Opponents")
    plt.ylabel("Win Rate (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    winrate_path = os.path.join(OUTPUT_DIR, "win_rate.png")
    plt.savefig(winrate_path, dpi=120, bbox_inches="tight")
    plt.close()

    # Plot 2: Average Score Difference
    plt.figure(figsize=(6, 4))
    plt.bar(opponents, avg_diffs, color="orange")
    plt.title("Average Score Difference (Black - White)")
    plt.ylabel("Score Difference")
    plt.axhline(0, color="gray", linewidth=1)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    diff_path = os.path.join(OUTPUT_DIR, "score_difference.png")
    plt.savefig(diff_path, dpi=120, bbox_inches="tight")
    plt.close()

    print(f"✅ Charts saved to:\n  - {winrate_path}\n  - {diff_path}")

if __name__ == "__main__":
    analyze()
