"use client";

import React, { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import BoardDisplay from "@/components/BoardDisplay";
import AgentSelector from "@/components/AgentSelector";
import MoveLog from "@/components/MoveLog";
import { createGame, makeMove, aiMove } from "@/lib/api";

type Move = [number, number];
const BLACK = 1;
const WHITE = -1;

export default function PlayPage() {
  const [gameId, setGameId] = useState<string | null>(null);
  const [board, setBoard] = useState<number[][]>([]);
  const [toMove, setToMove] = useState<number>(BLACK);
  const [legalMoves, setLegalMoves] = useState<Move[]>([]);
  const [pieces, setPieces] = useState({ black: 2, white: 2 });
  const [agent, setAgent] = useState("minimax");

  const [log, setLog] = useState<string[]>([]);
  const [aiExplanation, setAiExplanation] = useState("");
  const [agentDescription, setAgentDescription] = useState("");
  const [aiThinking, setAiThinking] = useState(false);
  const [winnerInfo, setWinnerInfo] = useState<{
    winner: string;
    black: number;
    white: number;
  } | null>(null);

  const logRef = useRef<HTMLDivElement | null>(null);

  /* ----------------------- INIT GAME ----------------------- */
  useEffect(() => {
    (async () => {
      const data = await createGame();
      setGameId(data.game_id);
      setBoard(data.board);
      setToMove(data.to_move);
      setLegalMoves(data.legal_moves || []);
      setPieces(data.pieces || { black: 2, white: 2 });
      setLog([`New game started (${data.game_id})`]);
    })();
  }, []);

  /* ----------------------- AGENT DESCRIPTION ----------------------- */
  useEffect(() => {
    const map: Record<string, string> = {
      random: "Chooses moves randomly.",
      greedy: "Maximizes immediate flips.",
      minimax: "Searches future positions for best outcome.",
      mcts: "Uses Monte Carlo rollouts to evaluate outcomes.",
      hybrid: "Greedy filter + Minimax + optional MCTS refinement."
    };
    setAgentDescription(map[agent] || "");
  }, [agent]);

  /* ----------------------- AUTO-SCROLL LOG ----------------------- */
  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [log]);

  /* ----------------------- HANDLE CELL CLICK ----------------------- */
  async function onCellClick(r: number, c: number) {
    if (!gameId || aiThinking || winnerInfo) return;

    const isLegal = legalMoves.some(([rr, cc]) => rr === r && cc === c);
    if (!isLegal) {
      setLog((x) => [...x, `Illegal move (${r},${c})`]);
      return;
    }

    try {
      const res = await makeMove(gameId, r, c);
      updateFromServer(res, `Human plays (${r},${c})`);

      if (res.to_move === WHITE && !winnerInfo) {
        await handleAIMove();
      }
    } catch {
      setLog((x) => [...x, `Move failed (${r},${c})`]);
    }
  }

  /* ----------------------- HANDLE PLAYER SKIP ----------------------- */
  async function handlePlayerSkip() {
    if (!gameId || aiThinking || winnerInfo) return;
    if (legalMoves.length > 0) return;

    setLog((x) => [...x, "Human skips turn"]);

    const res = await makeMove(gameId); // pass: backend handles it
    updateFromServer(res, null);

    if (res.to_move === WHITE && !winnerInfo) {
      await handleAIMove();
    }
  }

  /* ----------------------- HANDLE AI MOVE ----------------------- */
  async function handleAIMove() {
    if (!gameId || winnerInfo) return;

    setAiThinking(true);
    try {
      const res = await aiMove(gameId, agent, 1.5);
      updateFromServer(res, res.move ? `${agent.toUpperCase()} plays ${res.move}` : `${agent.toUpperCase()} skips`);

      if (res.move) explainAIMove(agent, res.move);
    } catch {
      setLog((x) => [...x, "AI move failed"]);
    }
    setTimeout(() => setAiThinking(false), 300);
  }

  /* ----------------------- UPDATE STATE FROM BACKEND ----------------------- */
  function updateFromServer(res: any, logLine: string | null) {
    setBoard(res.board);
    setToMove(res.to_move);
    setLegalMoves(res.legal_moves || []);
    setPieces(res.pieces || { black: 2, white: 2 });

    if (logLine) setLog((x) => [...x, logLine]);

    checkWinner(res.board);
  }

  /* ----------------------- AI MOVE EXPLANATION ----------------------- */
  function explainAIMove(agentType: string, move: Move) {
    const [r, c] = move;
    const msg: Record<string, string> = {
      random: `Played (${r},${c}) by random choice.`,
      greedy: `Played (${r},${c}) to maximize immediate flips.`,
      minimax: `Played (${r},${c}) after searching future states.`,
      mcts: `Played (${r},${c}) using Monte Carlo rollout statistics.`,
      hybrid: `Played (${r},${c}) via Greedy + Minimax (+MCTS).`,
    };
    setAiExplanation(msg[agentType] || "");
  }

  /* ----------------------- WIN CHECK ----------------------- */
  function checkWinner(boardState: number[][]) {
    const flat = boardState.flat();
    if (flat.includes(0)) return;

    const black = flat.filter((v) => v === BLACK).length;
    const white = flat.filter((v) => v === WHITE).length;

    let winner = "Draw";
    if (black > white) winner = "BLACK wins!";
    else if (white > black) winner = "WHITE wins!";

    setWinnerInfo({ winner, black, white });
    setLog((l) => [...l, `Game over → ${winner} (${black} vs ${white})`]);
  }

  /* ----------------------- UI ----------------------- */
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-green-950 via-black to-gray-900 text-white p-6">
      <div className="w-full max-w-6xl flex flex-col items-center gap-6">

        {/* Top bar */}
        <div className="flex items-center gap-4 w-full justify-between">
          <button onClick={() => location.reload()} className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded">
            New Game
          </button>

          <AgentSelector value={agent} onChange={setAgent} />

          <button
            onClick={handlePlayerSkip}
            disabled={legalMoves.length !== 0 || aiThinking}
            className={`px-3 py-1 rounded ${
              legalMoves.length === 0 && !aiThinking ? "bg-orange-600 hover:bg-orange-700" : "bg-gray-600 cursor-not-allowed"
            }`}
          >
            Skip Turn
          </button>

          <div className="ml-auto text-sm font-medium">
            Turn: {toMove === BLACK ? "BLACK" : "WHITE"}
          </div>
        </div>

        <div className="text-sm font-medium">
          Black: {pieces.black} | White: {pieces.white}
        </div>

        <div className="flex flex-wrap justify-center gap-8 mt-6 relative">
          {aiThinking && (
            <div className="absolute top-[-2rem] text-sm text-gray-400 animate-pulse">
              {agent.toUpperCase()} is thinking...
            </div>
          )}

          <BoardDisplay board={board} onCellClick={onCellClick} legalMoves={legalMoves} />

          <div className="flex flex-col gap-4 w-80">
            <MoveLog lines={log} logRef={logRef} />

            <div className="bg-gray-800 p-3 rounded shadow-md">
              <h3 className="font-semibold mb-1 text-yellow-400">AI Strategy</h3>
              <p className="text-sm text-gray-300">{agentDescription}</p>
            </div>

            <div className="bg-gray-800 p-3 rounded shadow-md">
              <h3 className="font-semibold mb-1 text-blue-400">AI Move Reasoning</h3>
              <p className="text-sm text-gray-300 min-h-[40px]">{aiExplanation || "Waiting..."}</p>
            </div>
          </div>
        </div>

        <AnimatePresence>
          {winnerInfo && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50"
            >
              <motion.div
                initial={{ y: -20 }}
                animate={{ y: 0 }}
                className="bg-gray-900 text-white p-8 rounded-xl shadow-lg text-center border border-gray-700"
              >
                <h2 className="text-2xl font-bold mb-2">{winnerInfo.winner}</h2>
                <p className="text-gray-300 mb-1">
                  BLACK: {winnerInfo.black} | WHITE: {winnerInfo.white}
                </p>
                <button
                  onClick={() => location.reload()}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
                >
                  New Game
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
