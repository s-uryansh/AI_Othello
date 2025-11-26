# **AI Othello**

This project is a complete **AI-powered Othello game**, featuring a Python backend with multiple AI agents and a modern Next.js frontend.
Players can play against different AI strategies such as **Random, Greedy, Minimax, MCTS, and Hybrid**.

---

## Clone the Repository

```sh
git clone https://github.com/s-uryansh/AI_Othello.git
cd AI_Othello
```

---

## Backend 

```sh
cd backend
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at:
**[http://localhost:8000](http://localhost:8000/docs)**

---

## Frontend

```sh
cd frontend
npm install
npm run dev
```

Frontend runs at:
**[http://localhost:3000](http://localhost:3000)**

---

## Run tests and collect logs

A helper script bundles backend test output, demo runs, and generated logs into logs/collected/.

From the repository root run:

```sh
# make script executable once
chmod +x ./scripts/run_all_tests.sh

# run tests and gather logs
./scripts/run_all_tests.sh
```

Collected artifacts will be written under ./logs/collected/ with timestamped files:
- backend_pytest_*.log
- demo_all_agents_*.log
- analyze_validation_*.log
- backend_app_logs_*/ (copied app/logs contents)

Notes:
- The script runs backend commands with PYTHONPATH=. so you should have backend dependencies installed (pip install -r backend/requirements.txt).
- Frontend build is optional and commented out in the script; enable if you have Node/npm available.

---

## Project Summary

AI Othello is a full-featured board game system where the backend performs all game logic legal moves, and AI decisions. The Python backend includes AI agents (Greedy, Minimax, MCTS, and a Hybrid approach). The frontend interacts with these agents through API calls, allowing the user to play, visualize moves, switch AI types, and track game progress in real time.