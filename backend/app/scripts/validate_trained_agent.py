from __future__ import annotations
import json
import os
from app.api.services.match_runner import MatchRunner
from app.core.eval.evaluator import Evaluator
from app.core.ai.minimax_agent import MinimaxAgent

LOG_DIR = "app/logs/validation"
TRAINED_WEIGHTS = "app/logs/training/trained_weights.json"
os.makedirs(LOG_DIR, exist_ok=True)

def load_trained_evaluator() -> Evaluator:
    if not os.path.exists(TRAINED_WEIGHTS):
        raise FileNotFoundError(f"Missing {TRAINED_WEIGHTS}")
    with open(TRAINED_WEIGHTS, "r") as f:
        weights = json.load(f)

    # Evaluator now expects dict-based weights
    ev = Evaluator(weights=weights)
    return ev

def validate_agent():
    print("\n=== VALIDATING TRAINED AGENT ===")
    evaluator = load_trained_evaluator()

    trained_agent = MinimaxAgent(evaluator, max_depth=4, time_limit=1.5)

    opponents = ["random", "greedy", "minimax"]
    results_summary = {}

    for opp in opponents:
        print(f"\n--- Match: TRAINED vs {opp.upper()} ---")
        match = MatchRunner(a1_name="minimax", a2_name=opp, games=4, time_limit=1.5)
        match.agent1 = trained_agent
        res = match.run()
        results_summary[opp] = res
        print(f"Result: {res['wins']} | Avg diff: {res['avg_score_diff']:.2f}")

    summary_path = f"{LOG_DIR}/validation_summary.json"
    with open(summary_path, "w") as f:
        json.dump(results_summary, f, indent=4)

    print(f"\n✅ Validation complete. Summary saved at {summary_path}")

if __name__ == "__main__":
    validate_agent()
