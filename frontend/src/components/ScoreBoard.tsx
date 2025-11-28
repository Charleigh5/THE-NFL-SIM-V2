import { useSimulationStore } from "../store/useSimulationStore";

export const ScoreBoard = () => {
  const { gameState } = useSimulationStore();

  return (
    <div className="flex items-center justify-between bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-4 w-full max-w-2xl mx-auto">
      {/* Home Team */}
      <div className="flex flex-col items-center w-1/3">
        <div className="text-3xl font-bold text-white">
          {gameState.homeScore}
        </div>
        <div className="text-sm text-gray-400 uppercase tracking-wider">
          Empire
        </div>
        {gameState.possession === "home" && (
          <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 animate-pulse" />
        )}
      </div>

      {/* Game Info */}
      <div className="flex flex-col items-center w-1/3 border-x border-white/10">
        <div className="text-xl font-mono text-cyan-400 font-bold">
          Q{gameState.quarter}
        </div>
        <div className="text-xs text-gray-500 mt-1">
          {gameState.down === 1
            ? "1st"
            : gameState.down === 2
            ? "2nd"
            : gameState.down === 3
            ? "3rd"
            : "4th"}{" "}
          & {gameState.distance}
        </div>
      </div>

      {/* Away Team */}
      <div className="flex flex-col items-center w-1/3">
        <div className="text-3xl font-bold text-white">
          {gameState.awayScore}
        </div>
        <div className="text-sm text-gray-400 uppercase tracking-wider">
          Genesis
        </div>
        {gameState.possession === "away" && (
          <div className="w-2 h-2 bg-cyan-400 rounded-full mt-2 animate-pulse" />
        )}
      </div>
    </div>
  );
};
