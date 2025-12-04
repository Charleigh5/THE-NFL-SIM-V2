import React from "react";
import "./ChemistryBadge.css";

interface ChemistryBadgeProps {
  level: number; // 0.0 to 1.0
  consecutiveGames: number;
  status: string; // "NONE", "DEVELOPING", "STRONG", "ELITE", "MAXIMUM"
  bonuses?: {
    pass_block: number;
    run_block: number;
    awareness: number;
  };
}

export const ChemistryBadge: React.FC<ChemistryBadgeProps> = ({
  level,
  consecutiveGames,
  status,
  bonuses,
}) => {
  const getStatusClass = (status: string) => {
    return status.toLowerCase();
  };

  return (
    <div className="relative inline-block">
      <div className={`chemistry-badge ${getStatusClass(status)}`}>
        <span className="mr-1">⚗️</span>
        {status} ({Math.round(level * 100)}%)
        <div className="chemistry-tooltip">
          <div className="tooltip-header">
            <span className="font-bold">OL Unit Chemistry</span>
            <span className="text-gray-400">{consecutiveGames} Games</span>
          </div>

          <div className="tooltip-body">
            <div className="tooltip-stat">
              <span>Status</span>
              <span className={`font-bold text-${getStatusClass(status)}`}>{status}</span>
            </div>

            {bonuses && (
              <>
                <div className="mt-2 text-xs text-gray-400 uppercase tracking-wider mb-1">
                  Bonuses
                </div>
                <div className="tooltip-stat bonus">
                  <span>Pass Block</span>
                  <span>+{bonuses.pass_block.toFixed(1)}</span>
                </div>
                <div className="tooltip-stat bonus">
                  <span>Run Block</span>
                  <span>+{bonuses.run_block.toFixed(1)}</span>
                </div>
                <div className="tooltip-stat bonus">
                  <span>Awareness</span>
                  <span>+{bonuses.awareness.toFixed(1)}</span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
