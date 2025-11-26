from __future__ import annotations
import random
import json
import os
from typing import Dict, List, Tuple
from app.api.services.match_runner import MatchRunner
from app.core.eval.evaluator import Evaluator

LOG_DIR = "app/logs/training"
os.makedirs(LOG_DIR, exist_ok=True)

class GATrainer:
    def __init__(
        self,
        base_agent: str = "minimax",
        opponent_agent: str = "greedy",
        population_size: int = 8,
        generations: int = 5,
        mutation_rate: float = 0.3,
        crossover_rate: float = 0.7,
    ) -> None:
        self.base_agent = base_agent
        self.opponent_agent = opponent_agent
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.feature_names = ["disc_diff", "mobility", "corner_occupancy", "corner_adj", "frontier"]

    def _random_weights(self) -> Dict[str, float]:
        """Generate random weight set."""
        return {f: random.uniform(-20, 20) for f in self.feature_names}

    def _mutate(self, weights: Dict[str, float]) -> Dict[str, float]:
        """Mutate random weights slightly."""
        for k in weights:
            if random.random() < self.mutation_rate:
                weights[k] += random.uniform(-5, 5)
        return weights

    def _crossover(self, w1: Dict[str, float], w2: Dict[str, float]) -> Dict[str, float]:
        """Combine two parents into a child."""
        child = {}
        for k in self.feature_names:
            if random.random() < self.crossover_rate:
                child[k] = w1[k]
            else:
                child[k] = w2[k]
        return child

    def _fitness(self, weights: Dict[str, float]) -> float:
        """Play against opponent agent and return average score difference."""
        evaluator = Evaluator(weights)
        runner = MatchRunner(self.base_agent, self.opponent_agent, games=2, time_limit=1.0, log=False)
        runner.agent1.evaluator = evaluator 
        results = runner.run()
        return results["avg_score_diff"]

    def train(self) -> Dict[str, float]:
        """Run the GA evolution loop."""
        population = [self._random_weights() for _ in range(self.population_size)]

        # Ensure we always have a valid Dict[str,float] to return (avoid None)
        best_weights: Dict[str, float] = population[0]
        best_score = float("-inf")

        for gen in range(1, self.generations + 1):
            print(f"\n=== Generation {gen}/{self.generations} ===")
            scored_pop: List[Tuple[Dict[str, float], float]] = []
            for w in population:
                score = self._fitness(w)
                scored_pop.append((w, score))
                print(f"Candidate {w} → fitness {score:.2f}")

            scored_pop.sort(key=lambda x: x[1], reverse=True)
            if scored_pop[0][1] > best_score:
                best_score = scored_pop[0][1]
                best_weights = scored_pop[0][0]

            survivors = [w for w, _ in scored_pop[: self.population_size // 2]]
            new_population = survivors.copy()

            while len(new_population) < self.population_size:
                p1, p2 = random.sample(survivors, 2)
                child = self._crossover(p1, p2)
                child = self._mutate(child)
                new_population.append(child)

            population = new_population

            print(f"Best in generation {gen}: {best_weights} with fitness {best_score:.2f}")

        # Save best weights
        out_file = os.path.join(LOG_DIR, "trained_weights.json")
        with open(out_file, "w") as f:
            json.dump(best_weights, f, indent=4)
        print(f"\nTraining complete. Best weights saved to {out_file}")
        return best_weights
