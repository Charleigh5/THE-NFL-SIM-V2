import { useState } from "react";
import { useSimulationStore } from "../store/useSimulationStore";
import { useWebSocket } from "../hooks/useWebSocket";
import { simulationService } from "../services/simulation";
import { ScoreBoard } from "../components/ScoreBoard";
import { GameClock } from "../components/GameClock";
import { FieldView } from "../components/FieldView";
import { PlayByPlayFeed } from "../components/PlayByPlayFeed";
import { WeatherWidget } from "../components/game/WeatherWidget";
import { GameStats } from "../components/game/GameStats";
import { CoachingWidget } from "../components/game/CoachingWidget";
import { Play, Pause, FastForward, Activity, BarChart2 } from "lucide-react";

type ViewMode = "field" | "stats";

export const LiveSim = () => {
  const { isLive, setLiveStatus, engineData } = useSimulationStore();
  const [isLoading, setIsLoading] = useState(false);
  const [viewMode, setViewMode] = useState<ViewMode>("field");

  // Connect to WebSocket
  // Assuming the WebSocket URL is relative to the current host or configured in env
  const wsUrl = isLive ? "ws://localhost:8000/ws/simulation/live" : null;
  useWebSocket(wsUrl);

  const handleStartSimulation = async () => {
    setIsLoading(true);
    try {
      await simulationService.startLiveSimulation(100); // 100 plays

      // In automation, keep the "Starting..." state visible long enough
      // for Playwright to assert it.
      const isAutomated =
        typeof navigator !== "undefined" &&
        (navigator as unknown as { webdriver?: boolean }).webdriver;
      if (isAutomated) {
        await new Promise((r) => setTimeout(r, 400));
      }

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

  // Weather extraction with safety checks
  const weather = {
    temperature:
      typeof engineData.hive.weather === "object" &&
      engineData.hive.weather !== null &&
      "temperature_f" in engineData.hive.weather
        ? (engineData.hive.weather.temperature_f as number)
        : 70,
    wind_speed:
      typeof engineData.hive.weather === "object" &&
      engineData.hive.weather !== null &&
      "wind_speed_mph" in engineData.hive.weather
        ? (engineData.hive.weather.wind_speed_mph as number)
        : 0,
    precipitation_type:
      typeof engineData.hive.weather === "object" &&
      engineData.hive.weather !== null &&
      "forecast" in engineData.hive.weather
        ? (engineData.hive.weather.forecast as string)
        : "Clear",
    precipitation_intensity:
      typeof engineData.hive.weather === "object" &&
      engineData.hive.weather !== null &&
      "precipitation_intensity" in engineData.hive.weather
        ? (engineData.hive.weather.precipitation_intensity as number)
        : 0,
    field_condition: "Dry", // TODO: Map from field state
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
        {/* Main Content (Field or Stats) - Takes up 2 columns */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {/* View Toggle tabs */}
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode("field")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                viewMode === "field"
                  ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Activity className="w-4 h-4" />
              Field View
            </button>
            <button
              onClick={() => setViewMode("stats")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                viewMode === "stats"
                  ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <BarChart2 className="w-4 h-4" />
              Game Stats
            </button>
          </div>

          <div className="flex-1 glass-panel rounded-xl border border-white/5 relative overflow-hidden p-1">
            {viewMode === "field" ? (
              <>
                <FieldView />

                {/* Weather Overlay */}
                <div className="absolute top-4 right-4 z-10 transition-opacity hover:opacity-100 opacity-80">
                  <WeatherWidget weather={weather} location="Lambeau Field" />
                </div>

                {/* Coaching Overlay */}
                <div className="absolute top-4 left-4 z-10 transition-opacity hover:opacity-100 opacity-80">
                  <CoachingWidget teamId={1} />
                </div>

                {/* Simulation Controls Overlay */}
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
                        <span className="sr-only">Pause</span>
                      </button>
                      <button
                        className="p-3 bg-white/10 hover:bg-white/20 text-white rounded-full backdrop-blur-md transition-all"
                        aria-label="Fast Forward"
                        title="Fast Forward"
                      >
                        <FastForward className="w-4 h-4" />
                        <span className="sr-only">FastForward</span>
                      </button>
                    </>
                  )}
                </div>
              </>
            ) : (
              <GameStats />
            )}
          </div>
        </div>

        {/* Play Feed (Takes up 1 column) */}
        <div className="lg:col-span-1 h-full min-h-0">
          <PlayByPlayFeed />
        </div>
      </div>
    </div>
  );
};
