const BASE = process.env.NEXT_PUBLIC_API_URL || "https://ai-othello-4pw9.onrender.com/";

export type BoardResponse = {
  board: number[][];
  to_move: number;
  legal_moves?: [number, number][];
  game_id?: string;
};

export async function createGame() {
  const res = await fetch(`${BASE}/api/v1/game/new`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to create game");
  return res.json();
}

export async function makeMove(gameId: string, row?: number | null, col?: number | null) {
  const body: any = {};
  if (row !== undefined) body.row = row;
  if (col !== undefined) body.col = col;
  const res = await fetch(`${BASE}/api/v1/game/${gameId}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error("Move failed");
  return res.json();
}


export async function aiMove(gameId: string, agent = "minimax", time = 1.5) {
  const res = await fetch(`${BASE}/api/v1/game/${gameId}/ai_move?agent=${agent}&time=${time}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("AI move failed");
  return res.json();
}

export async function getState(gameId: string) {
  const res = await fetch(`${BASE}/api/v1/game/${gameId}/state`);
  if (!res.ok) throw new Error("Failed to get state");
  return res.json();
}
