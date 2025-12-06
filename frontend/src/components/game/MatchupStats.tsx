import React from 'react';

interface MatchupStatsProps {
  attacker: {
    name: string;
    statName: string;
    statValue: number;
  };
  defender: {
    name: string;
    statName: string;
    statValue: number;
  };
}

export const MatchupStats: React.FC<MatchupStatsProps> = ({ attacker, defender }) => {
  return (
    <div className="bg-black/40 border border-white/10 rounded-lg p-3">
      <h4 className="text-xs text-cyan-400 font-bold uppercase mb-2 text-center">Key Matchup</h4>
      <div className="flex justify-between items-center text-sm">
        {/* Attacker */}
        <div className="text-left">
          <div className="text-white font-bold">{attacker.name}</div>
          <div className="text-gray-400 text-xs">
            {attacker.statName}: <span className="text-green-400">{attacker.statValue}</span>
          </div>
        </div>

        <div className="text-gray-600 font-bold px-2">VS</div>

        {/* Defender */}
        <div className="text-right">
          <div className="text-white font-bold">{defender.name}</div>
          <div className="text-gray-400 text-xs">
            <span className="text-red-400">{defender.statValue}</span> :{defender.statName}
          </div>
        </div>
      </div>

      {/* Comparison Bar */}
      <div className="mt-2 h-1.5 bg-gray-700 rounded-full flex overflow-hidden">
        <div
           className="bg-green-500 h-full"
           style={{ width: `${(attacker.statValue / (attacker.statValue + defender.statValue)) * 100}%` }}
        />
        <div
           className="bg-red-500 h-full"
           style={{ width: `${(defender.statValue / (attacker.statValue + defender.statValue)) * 100}%` }}
        />
      </div>
    </div>
  );
};
