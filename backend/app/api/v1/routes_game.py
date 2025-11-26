from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional
from app.core.engine.board import Board
from app.core.eval.evaluator import Evaluator
from app.core.ai.random_agent import RandomAgent
from app.core.ai.greedy_agent import GreedyAgent
from app.core.ai.minimax_agent import MinimaxAgent
from app.core.ai.mcts_agent import MCTSAgent
from app.core.ai.hybrid_agent import HybridAgent
import uuid
import os
import json

router = APIRouter()

GAMES = {}

AGENT_FACTORY = {
    "random": RandomAgent,
    "greedy": GreedyAgent,
    "minimax": MinimaxAgent,
    "mcts": MCTSAgent,
    "hybrid": HybridAgent,
    "minimax_ga": MinimaxAgent,
}


def _make_agent_by_name(name: str, evaluator: Evaluator, time_limit: float):
    name = name.lower()
    cls = AGENT_FACTORY.get(name)
    if not cls:
        raise ValueError(f"Unknown agent '{name}'")
    # instantiate with sensible defaults / evaluator when required
    if name == "random":
        return cls()
    if name == "greedy":
        return cls(evaluator)
    if name == "minimax" or name == "minimax_ga":
        return cls(evaluator, max_depth=4, time_limit=time_limit)
    if name == "mcts":
        return cls(evaluator, simulations=400, time_limit=time_limit)
    if name == "hybrid":
        return cls(evaluator, use_mcts=True, deep_depth=4, time_limit=time_limit)
    return cls()


def _pieces_dict(board: Board):
    b, w = board.score()
    return {"black": b, "white": w}


@router.post("/new")
def create_game():
    game_id = str(uuid.uuid4())
    board = Board()
    GAMES[game_id] = board
    return {
        "game_id": game_id,
        "board": board.grid,
        "to_move": board.to_move,
        "legal_moves": board.legal_moves(board.to_move),
        "pieces": _pieces_dict(board),
    }


@router.post("/{game_id}/move")
def make_move(game_id: str, data: dict = Body(...)):
    """
    Apply a move or a pass.
    Accepts JSON { "row": int, "col": int } or {} / { "row": null, "col": null } for pass.
    """
    board = GAMES.get(game_id)
    if not board:
        raise HTTPException(status_code=404, detail="Game not found")

    # allow pass if row/col missing or explicitly null
    row = data.get("row") if isinstance(data, dict) else None
    col = data.get("col") if isinstance(data, dict) else None
    if row is None or col is None:
        # treat as pass
        board.apply_move(None, board.to_move)
    else:
        try:
            board.apply_move((int(row), int(col)), board.to_move)
        except ValueError:
            raise HTTPException(status_code=400, detail="Illegal move")

    return {
        "board": board.grid,
        "to_move": board.to_move,
        "legal_moves": board.legal_moves(board.to_move),
        "pieces": _pieces_dict(board),
    }


@router.post("/{game_id}/ai_move")
def ai_move(game_id: str, agent: Optional[str] = Query("minimax"), time: float = 1.5):
    """
    Ask backend to choose and apply an AI move for the side whose turn it is.
    Returns move (or null if pass), board, to_move, legal_moves, pieces, eval_score.
    """
    board = GAMES.get(game_id)
    if not board:
        raise HTTPException(status_code=404, detail="Game not found")

    if (agent or "").lower() == "minimax_ga":
        try:
            from app.api.services.validate_agent import load_trained_evaluator
            ev = load_trained_evaluator()
        except Exception:
            ev = Evaluator()  
    else:
        ev = Evaluator()

    try:
        ai = _make_agent_by_name(agent or "minimax", ev, time_limit=time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unknown agent")

    mv, score = ai.best_move(board, board.to_move)

    if mv is not None:
        try:
            board.apply_move(mv, board.to_move)
        except ValueError:
            board.apply_move(None, board.to_move)
            mv = None
    else:
        board.apply_move(None, board.to_move)

    return {
        "move": mv,
        "board": board.grid,
        "to_move": board.to_move,
        "legal_moves": board.legal_moves(board.to_move),
        "pieces": _pieces_dict(board),
        "eval_score": float(score) if score is not None else 0.0,
    }


@router.get("/{game_id}/state")
def get_state(game_id: str):
    board = GAMES.get(game_id)
    if not board:
        raise HTTPException(status_code=404, detail="Game not found")
    return {
        "board": board.grid,
        "to_move": board.to_move,
        "legal_moves": board.legal_moves(board.to_move),
        "pieces": _pieces_dict(board),
    }
