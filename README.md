# **AI Othello**

This project is a complete **AI-powered Othello game**, featuring a Python backend with multiple AI agents and a modern Next.js frontend.
Players can play against different AI strategies such as **Random, Greedy, Minimax, MCTS, and Hybrid**.

---

## Clone the Repository

```sh
git clone <your_repo_url>
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

## Project Summary

AI Othello is a full-featured board game system where the backend performs all game logic legal moves, and AI decisions. The Python backend includes AI agents (Greedy, Minimax, MCTS, and a Hybrid approach). The frontend interacts with these agents through API calls, allowing the user to play, visualize moves, switch AI types, and track game progress in real time.