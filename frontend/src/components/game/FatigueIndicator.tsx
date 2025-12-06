import React from 'react';
import { motion } from 'framer-motion';

interface FatigueIndicatorProps {
  playerName: string;
  fatigueLevel: number; // 0-100 (0 = Fresh, 100 = Exhausted)
  position: string;
}

export const FatigueIndicator: React.FC<FatigueIndicatorProps> = ({ playerName, fatigueLevel, position }) => {
  // Fatigue logic:
  // 0-20: Fresh (Green)
  // 21-50: Tired (Yellow)
  // 51+: Exhausted (Red)

  const getColor = (level: number) => {
    if (level < 20) return "bg-green-500";
    if (level < 50) return "bg-yellow-500";
    return "bg-red-500";
  };

  const widthPercentage = Math.max(0, Math.min(100, 100 - fatigueLevel));

  return (
    <div className="flex flex-col gap-1 w-full max-w-[200px] bg-black/40 p-2 rounded-lg border border-white/10">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold text-gray-200">{position} • {playerName}</span>
        <span className="text-gray-400">{Math.round(100 - fatigueLevel)}%</span>
      </div>

      <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          className={`h-full ${getColor(fatigueLevel)}`}
          initial={{ width: "100%" }}
          animate={{ width: `${widthPercentage}%` }}
          transition={{ duration: 0.5 }}
        />
      </div>
    </div>
  );
};
