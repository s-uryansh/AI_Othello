"use client";
import React from "react";

export default function AgentSelector({ value, onChange }: { value: string; onChange: (v: string) => void }) {
const agents = [
  "random",
  "greedy",
  "minimax",
  "minimax_ga",
  "mcts",
  "hybrid"
];
  return (
    <div className="flex items-center gap-2">
      <label className="text-sm">Agent</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="p-1 rounded border bg-white dark:bg-gray-800"
      >
        {agents.map((a) => (
          <option key={a} value={a}>
            {a}
          </option>
        ))}
      </select>
    </div>
  );
}
