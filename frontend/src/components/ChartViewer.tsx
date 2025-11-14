"use client";
import React from "react";

export default function ChartViewer() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-semibold mb-2">Win Rate</h3>
        <img src="/validation_plots/win_rate.png" alt="win rate" className="max-w-full rounded shadow" />
      </div>
      <div>
        <h3 className="font-semibold mb-2">Average Score Difference</h3>
        <img src="/validation_plots/score_difference.png" alt="score diff" className="max-w-full rounded shadow" />
      </div>
    </div>
  );
}
