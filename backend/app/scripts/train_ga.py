from app.api.services.trainer import GATrainer

def main():
    trainer = GATrainer(
        base_agent="minimax",
        opponent_agent="greedy",
        population_size=6,
        generations=4,
    )
    best = trainer.train()
    print("\nFinal optimized weights:", best)

if __name__ == "__main__":
    main()
