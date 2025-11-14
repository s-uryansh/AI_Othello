# Othello Backend
This `README.md` explain the working of backend for othello game which is written in Python

## Run
Run from root path (AI_Othello/backend)
-  `PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Working of different AIs

### Greedy AI Agent

1. Gets all the legal moves possible
2. If no moves -> pass the turn
3. After fetching all the legal moves, it temporarily applies all the moves, uses evaluator function to find the move which helps in maximizing the flipped discs.

### Hybrid AI  Agent
Instead of using one agent it is using three agents: `Greedy, Minimax and MCTS`

1. Greedy does a quick scan to find the good candidate move.
    - if greedy doesn't find any good moves it passes the turn
2. If `use_mcts=True`, the Hybrid Agent lets MCTS run many simulations to statistically find the move with the strongest long-term win probability. 
3. Otherwise `Minimax`  handles deep thinking
    - Minimax explores future moves 
    - Opponent's response
    - prunes bad branches
    
    `Minimax` selects the move which is best for future.
    This Agent: Prevents dumb move by greedy algorithm, MCTS adds exploration, Minimax gives tactical precision.

### MCTS AI Agent
The 4 step implementation of Monte Carlo Tree Search loop, using UCT. The algorithm simulates game on loop to estimate which move is most likely to win the game.

1. Starts with the root node which contains the copy of current game.
2. Go down the tree by choosing the child node with highest UCT until node with unexplored move is hit or terminated.
3. If the node has untried the legal move, pick one add new child for that move.
4. From the new node play the game to end using random moves or greedy approch 
5. Go back to root incrementing the visit count and adding the winsfor the node where the player just moved equals the simulated winner.
6. Repeat steps 2 to 5.
7. Pick the root child with highest value of visit count.

### Minimax AI Agent
This agent plays Othello using iterative-deepening Minimax with Alpha–Beta pruning plus a Transposition Table (TT).
It searches multiple layers of future positions, pruning bad branches early and caching evaluated states with Zobrist hashing to avoid duplicate work.

1. Start timer + clear cache before each move.
2. Search depth 1 → 2 → ... until time runs out.
3. For each legal move, run alpha-beta to evaluate deeper positions.
4. Stop exploring branches that cannot influence the final decision.
5. Generate a 64-bit hash for each board state.
6. Before searching a position, reuse stored evaluation if available.
7. Bounds (EXACT/LOWER/UPPER): store partial search results to prune even more aggressively.
8. Apply move → recurse → undo move for every explored branch.
9. when depth = 0 or no moves, return evaluator score from BLACK’s point of view.
10. Pick best move found at deepest completed depth before time expires.

### Random AI Agent
The RandomAgent simply chooses any legal move at random.
There is no strategy, no evaluation, and no prediction
1. Collect all legal moves for the current player.
2. If no moves exist, return pass.
3. Otherwise, choose one move uniformly at random.
4. Return that move with a neutral score (0.0).