# **Othello Frontend**

This is the frontend for the Othello AI project, built using **Next.js + React**.
It provides the UI for interacting with the backend game engine and AI.

## **Features**

* Displays an interactive 8×8 Othello board.
* Highlights all legal moves returned by the backend.
* Allows the human player to make moves by clicking on the board.
* Supports skipping a turn when the backend says no legal moves exist.
* Communicates with the backend to:

  * Start new games
  * Apply human moves
  * Request AI moves (Random, Greedy, Minimax, MCTS, Hybrid)
  * Fetch updated board state
* Shows piece counts for both players.
* Dropdown to select different AI agents.

## **Tech Stack**

* **Next.js**
* **React**
* **Framer Motion**

The frontend does **not** calculate rules or legal moves;
**all game logic comes from the backend**.
