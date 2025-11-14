import argparse
from app.api.services.match_runner import MatchRunner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a1", required=True, help="Agent 1 name (black)")
    parser.add_argument("--a2", required=True, help="Agent 2 name (white)")
    parser.add_argument("--games", type=int, default=5, help="Number of games")
    parser.add_argument("--time", type=float, default=1.5, help="Time limit per move")
    args = parser.parse_args()

    runner = MatchRunner(args.a1, args.a2, games=args.games, time_limit=args.time)
    results = runner.run()
    print("\n=== Match Summary ===")
    print(results)

if __name__ == "__main__":
    main()
