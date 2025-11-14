"use client";
import { motion, AnimatePresence } from "framer-motion";

export type BoardGrid = number[][];
export type Move = [number, number];

interface Props {
  board: BoardGrid;
  onCellClick?: (r: number, c: number) => void;
  legalMoves?: Move[];
  size?: number;
}

export default function BoardDisplay({ board, onCellClick, legalMoves = [], size = 48 }: Props) {
  const s = board.length;
  const legalSet = new Set(legalMoves.map(([r, c]) => `${r}:${c}`));

  return (
    <div className="inline-block bg-green-700 p-2 rounded-md shadow-lg">
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${s}, ${size}px)`,
          gap: "4px",
        }}
      >
        {board.map((row, r) =>
          row.map((cell, c) => {
            const key = `${r}-${c}`;
            const isLegal = legalSet.has(`${r}:${c}`);

            return (
              <div
                key={key}
                onClick={() => onCellClick?.(r, c)}
                className="flex items-center justify-center cursor-pointer"
                style={{
                  width: size,
                  height: size,
                  background: "#0b6b3a",
                  borderRadius: "6px",
                  boxShadow: "inset 0 0 0 1px rgba(0,0,0,0.25)",
                }}
              >
                <AnimatePresence mode="popLayout">
                  {cell !== 0 && (
                    <motion.div
                      key={`${r}-${c}-${cell}`}
                      initial={{ scale: 0, opacity: 0, rotateY: 180 }}
                      animate={{ scale: 1, opacity: 1, rotateY: 0 }}
                      exit={{ scale: 0, opacity: 0 }}
                      transition={{ duration: 0.3, ease: "easeOut" }}
                      className={`w-10 h-10 rounded-full shadow-md ${
                        cell === 1 ? "bg-black" : "bg-white"
                      }`}
                    />
                  )}
                </AnimatePresence>

                {cell === 0 && isLegal && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 0.7 }}
                    className="w-3 h-3 rounded-full bg-yellow-300"
                  />
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
