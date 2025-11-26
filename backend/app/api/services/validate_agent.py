from __future__ import annotations
import json
import os
from app.core.eval.evaluator import Evaluator

TRAINED_WEIGHTS = os.path.join("app", "logs", "training", "trained_weights.json")

def load_trained_evaluator() -> Evaluator:
    """
    Load trained weights and return an Evaluator configured with them.
    Raises FileNotFoundError if weights are missing so callers can fallback.
    """
    if not os.path.exists(TRAINED_WEIGHTS):
        raise FileNotFoundError(f"Missing {TRAINED_WEIGHTS}")
    with open(TRAINED_WEIGHTS, "r") as f:
        weights = json.load(f)
    return Evaluator(weights=weights)
