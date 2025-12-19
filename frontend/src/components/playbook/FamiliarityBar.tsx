import React from "react";
import { motion } from "framer-motion";
import { FamiliarityLevel, getFamiliarityLevel } from "../../types/playbook";

interface FamiliarityBarProps {
  score: number; // 0.0 to 1.0
  showLabel?: boolean;
}

export const FamiliarityBar: React.FC<FamiliarityBarProps> = ({ score, showLabel = true }) => {
  const level = getFamiliarityLevel(score);
  const percentage = Math.round(score * 100);

  const getColor = (lvl: FamiliarityLevel) => {
    switch (lvl) {
      case FamiliarityLevel.EXPERT:
        return "bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.4)]";
      case FamiliarityLevel.VETERAN:
        return "bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.4)]";
      case FamiliarityLevel.UNFAMILIAR:
      default:
        return "bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.4)]";
    }
  };

  const getLabelColor = (lvl: FamiliarityLevel) => {
    switch (lvl) {
      case FamiliarityLevel.EXPERT:
        return "text-green-400";
      case FamiliarityLevel.VETERAN:
        return "text-yellow-400";
      case FamiliarityLevel.UNFAMILIAR:
      default:
        return "text-red-400";
    }
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between items-end mb-1">
          <span className="text-[10px] uppercase text-gray-500 font-bold tracking-wider">
            Familiarity
          </span>
          <span className={`text-xs font-bold ${getLabelColor(level)} flex items-center gap-1`}>
            {percentage}% <span className="text-[9px] opacity-70">({level})</span>
          </span>
        </div>
      )}
      <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${getColor(level)}`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>
    </div>
  );
};
