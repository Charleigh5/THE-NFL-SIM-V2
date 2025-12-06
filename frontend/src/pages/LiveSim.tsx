import { useState } from "react";
import { useSimulationStore } from "../store/useSimulationStore";
import { useWebSocket } from "../hooks/useWebSocket";
import { simulationService } from "../services/simulation";
import { ScoreBoard } from "../components/ScoreBoard";
import { GameClock } from "../components/GameClock";
import { FieldView } from "../components/FieldView";
import { PlayByPlayFeed } from "../components/PlayByPlayFeed";
import { WeatherWidget } from "../components/game/WeatherWidget";
import { FatigueIndicator } from "../components/game/FatigueIndicator";
import { MatchupStats } from "../components/game/MatchupStats";
import { Play, Pause, FastForward } from "lucide-react";

export const LiveSim = () => {
  const { isLive, setLiveStatus, gameState, playLog } = useSimulationStore();
  const [isLoading, setIsLoading] = useState(false);

  // Connect to WebSocket
  // Assuming the WebSocket URL is relative to the current host or configured in env
  const wsUrl = "ws://localhost:8000/ws/simulation/live";
  useWebSocket(wsUrl);

  const handleStartSimulation = async () => {
    setIsLoading(true);
    try {
      await simulationService.startLiveSimulation(100); // 100 plays
      setLiveStatus(true);
      console.log("Live simulation started - receiving WebSocket updates");
    } catch (error) {
      console.error("Failed to start simulation:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopSimulation = async () => {
    try {
      await simulationService.stopSimulation();
      setLiveStatus(false);
      console.log("Simulation stopped");
    } catch (error) {
      console.error("Failed to stop simulation:", error);
    }
  };

  return (
    <div className="h-full flex flex-col gap-6 p-6">
      {/* Header Area */}
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Live Simulation</h1>
          <p className="text-cyan-400/80 text-sm">Week 4: Empire vs. Genesis</p>
        </div>
        <GameClock />
      </header>

      {/* Scoreboard */}
      <ScoreBoard />

      {/* Main Game Area */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-0">
        {/* Field View (Takes up 2 columns) */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          <div className="flex-1 glass-panel rounded-xl border border-white/5 relative overflow-hidden p-1">
            <FieldView />

            {/* Weather Overlay */}
            <div className="absolute top-4 right-4 z-10">
              <WeatherWidget
                temperature={35}
                condition="Snow"
                windSpeed={12}
                location="Lambeau Field"
              />
            </div>

            {/* Overlay Controls */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2 z-20">
              {!isLive ? (
                <button
                  onClick={handleStartSimulation}
                  disabled={isLoading}
                  className="flex items-center gap-2 px-6 py-2 bg-green-500 hover:bg-green-400 text-black font-bold rounded-full transition-all shadow-lg shadow-green-500/20"
                >
                  <Play className="w-4 h-4" />
                  {isLoading ? "Starting..." : "KICKOFF"}
                </button>
              ) : (
                <>
                  <button
                    onClick={handleStopSimulation}
                    className="p-3 bg-red-500 hover:bg-red-400 text-white rounded-full backdrop-blur-md transition-all shadow-lg"
                    aria-label="Pause Simulation"
                    title="Pause Simulation"
                  >
                    <Pause className="w-4 h-4" />
                  </button>
                  <button
                    className="p-3 bg-white/10 hover:bg-white/20 text-white rounded-full backdrop-blur-md transition-all"
                    aria-label="Fast Forward"
                    title="Fast Forward"
                  >
                    <FastForward className="w-4 h-4" />
                  </button>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Play Feed (Takes up 1 column) */}
        <div className="lg:col-span-1 h-full min-h-0 flex flex-col gap-4">
          <PlayByPlayFeed />

          {/* Key Matchup (Mock Data for now until backend sends specific matchup data) */}
          <MatchupStats
             attacker={{ name: "D. Hopkins", statName: "Route Running", statValue: 92 }}
             defender={{ name: "J. Ramsey", statName: "Man Coverage", statValue: 94 }}
          />

          {/* Key Player Fatigue (Dynamic based on last play) */}
          {playLog.length > 0 && gameState.playerFatigue && (
            <div className="bg-black/20 backdrop-blur-sm border border-white/5 rounded-xl p-4">
               <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">Player Energy</h3>
               <div className="flex flex-col gap-2">
                 {/* Try to show players from the last play */}
                 {(() => {
                    const lastPlay = playLog[0];
                    const playersToShow = [];

                    if (lastPlay.passer_id) playersToShow.push({ id: lastPlay.passer_id, role: "QB" });
                    if (lastPlay.rusher_id) playersToShow.push({ id: lastPlay.rusher_id, role: "RB" });
                    if (lastPlay.receiver_id) playersToShow.push({ id: lastPlay.receiver_id, role: "WR" });

                    // Limit to 3
                    return playersToShow.slice(0, 3).map(p => {
                       const fatigue = gameState.playerFatigue?.[String(p.id)] ?? 0;
                       return (
                         <FatigueIndicator
                           key={p.id}
                           playerName={`Player ${p.id}`} // We'd need a roster lookup here for real names
                           position={p.role}
                           fatigueLevel={fatigue}
                         />
                       );
                    });
                 })()}
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
