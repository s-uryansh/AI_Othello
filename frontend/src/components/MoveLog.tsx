"use client";
import React, { RefObject } from "react";

export default function MoveLog({
  lines,
  logRef,
}: {
  lines: string[];
  logRef?: React.RefObject<HTMLDivElement | null>;
}) {
  return (
    <div
      ref={logRef}
      className="bg-gray-900 text-white p-3 rounded h-64 overflow-auto text-sm w-80 shadow-inner border border-gray-700"
    >
      {lines.length === 0 ? (
        <div className="text-gray-500 text-center">No moves yet</div>
      ) : (
        lines.map((l, i) => (
          <div key={i} className="py-0.5">
            {l}
          </div>
        ))
      )}
    </div>
  );
}
