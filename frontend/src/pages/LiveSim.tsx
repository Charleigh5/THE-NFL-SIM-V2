import { useState, useRef } from "react";
import { useSimulationStore } from "../store/useSimulationStore";
import { useWebSocket } from "../hooks/useWebSocket";
import { simulationService } from "../services/simulation";
import { ScoreBoard } from "../components/ScoreBoard";
import { GameClock } from "../components/GameClock";
import { FieldCanvas } from "../components/game/FieldCanvas";
import type { FieldCanvasRef } from "../components/game/FieldCanvas";
import { PlayByPlayFeed } from "../components/PlayByPlayFeed";
import { PhysicsDebugOverlay } from "../components/debug/PhysicsDebugOverlay";
import { WeatherWidget } from "../components/game/WeatherWidget";
import { GameStats } from "../components/game/GameStats";
import { CoachingWidget } from "../components/game/CoachingWidget";
import { MomentumIndicator } from "../components/game/MomentumIndicator";
import { CrowdNoiseMeter } from "../components/game/CrowdNoiseMeter";
import { GridironVisualizer } from "../components/GridironVisualizer";
import { LiveGameVisualizer } from "../components/3d/LiveGameVisualizer";
import { ReplayScrubber } from "../components/game/ReplayScrubber";
import { PlayAnimator } from "../components/3d/PlayAnimator";
import { soundEffects } from "../services/soundEffects";
import { Play, Pause, FastForward, Activity, BarChart2, Layers, Tv } from "lucide-react";

type ViewMode = "field" | "stats" | "gridiron" | "3d";

export const LiveSim = () => {
  const { isLive, setLiveStatus, engineData, gameState } = useSimulationStore();
  const [isLoading, setIsLoading] = useState(false);
  const [viewMode, setViewMode] = useState<ViewMode>("field");
  const canvasRef = useRef<FieldCanvasRef | null>(null);

  const wsUrl = isLive ? "ws://localhost:8000/ws/simulation/live" : null;
  useWebSocket(wsUrl);

  const handleStartSimulation = async () => {
    soundEffects.playWhistle();
    soundEffects.playCrowdRoar();
    setIsLoading(true);
    try {
      await simulationService.startLiveSimulation(100);

      const isAutomated =
        typeof navigator !== "undefined" &&
        (navigator as unknown as { webdriver?: boolean }).webdriver;
      if (isAutomated) {
        await new Promise((r) => setTimeout(r, 400));
      }

      setLiveStatus(true);
    } catch (error) {
      console.error("Failed to start simulation:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopSimulation = async () => {
    soundEffects.playStadiumHorn();
    try {
      await simulationService.stopSimulation();
      setLiveStatus(false);
    } catch (error) {
      console.error("Failed to stop simulation:", error);
    }
  };

  // Mock Trajectory for F-032 Verification
  const [mockTrajectory] = useState(generateMockPlay());

  function generateMockPlay() {
    const frames = [];
    for (let i = 0; i < 120; i++) {
      frames.push({
        frame_id: i,
        timestamp: i / 60,
        ball: { position: { x: 20 + i * 0.1, y: 26 }, height: 0, rotation: 0 },
        events: [],
        players: [
          {
            player_id: 1,
            position: { x: 20 + i * 0.05, y: 26 },
            velocity: { x: 0, y: 0 },
            orientation: 0,
            state: "RUN" as const,
          },
          {
            player_id: 12,
            position: { x: 25 - i * 0.02, y: 26 },
            velocity: { x: 0, y: 0 },
            orientation: 3.14,
            state: "IDLE" as const,
          },
        ],
      });
    }
    return { play_id: "test", frames, duration: 2.0 };
  }

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
    field_condition: "Dry",
  };

  return (
    <div className="h-full flex flex-col gap-6 p-4 md:p-6 font-body">
      {/* Broadcast Header Area */}
      <header className="flex items-center justify-between border-b border-white/10 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-red-400">
              EA NextGen Broadcast • Live Game Day
            </span>
          </div>
          <h1 className="text-3xl md:text-4xl font-header uppercase tracking-tight text-white mt-0.5">
            Game Day Simulation
          </h1>
          <p className="text-gray-400 text-xs font-mono">
            Lambeau Field • Week 4 Primetime Matchup
          </p>
        </div>
        <GameClock />
      </header>

      {/* Broadcast Scoreboard & Momentum HUD */}
      <div className="flex flex-col gap-3">
        <div className="flex justify-between items-center px-4">
          <MomentumIndicator label="Home Momentum" state={gameState.homeMomentum} align="left" />
          <MomentumIndicator label="Away Momentum" state={gameState.awayMomentum} align="right" />
        </div>
        <ScoreBoard />
      </div>

      {/* Main Stadium Gridiron Arena */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-0">
        {/* Main Content (Field / Stats / Gridiron) */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {/* View Mode Switcher */}
          <div className="flex gap-2">
            <button
              onClick={() => {
                soundEffects.playSnap();
                setViewMode("field");
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-header uppercase tracking-wider transition-all ${
                viewMode === "field"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg shadow-red-600/30"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Activity className="w-4 h-4" />
              Field View
            </button>
            <button
              onClick={() => {
                soundEffects.playSnap();
                setViewMode("gridiron");
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-header uppercase tracking-wider transition-all ${
                viewMode === "gridiron"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg shadow-red-600/30"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Layers className="w-4 h-4" />
              Turf & S2 Cognition
            </button>
            <button
              onClick={() => {
                soundEffects.playSnap();
                setViewMode("3d");
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-header uppercase tracking-wider transition-all ${
                viewMode === "3d"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg shadow-red-600/30"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Tv className="w-4 h-4" />
              3D Live Cam
            </button>
            <button
              onClick={() => {
                soundEffects.playSnap();
                setViewMode("stats");
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-header uppercase tracking-wider transition-all ${
                viewMode === "stats"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg shadow-red-600/30"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <BarChart2 className="w-4 h-4" />
              Box Score
            </button>
          </div>

          {/* Viewport Canvas Container */}
          <div className="flex-1 broadcast-glass rounded-2xl border border-white/15 relative overflow-hidden p-1 shadow-2xl min-h-[420px]">
            {viewMode === "3d" ? (
              <div className="p-2">
                <LiveGameVisualizer gameId={1} enableBroadcast={true} />
              </div>
            ) : viewMode === "gridiron" ? (
              <div className="p-2">
                <GridironVisualizer />
              </div>
            ) : viewMode === "field" ? (
              <>
                <PhysicsDebugOverlay play={mockTrajectory} canvasRef={canvasRef} />
                <PlayAnimator
                  onAnimationComplete={() => console.log("Play telemetry animation complete")}
                />
                <FieldCanvas
                  ref={canvasRef}
                  isPlaying={isLive}
                  currentPlay={mockTrajectory}
                  playbackSpeed={1.0}
                  onPlayComplete={() => console.log("Play complete")}
                />

                {/* Replay Timeline Scrubber */}
                <div className="absolute bottom-20 left-1/2 -translate-x-1/2 z-20 w-80 max-w-[90%]">
                  <ReplayScrubber canvasRef={canvasRef} duration={mockTrajectory.duration || 2.0} />
                </div>

                {/* Weather Overlay */}
                <div className="absolute top-4 right-4 z-10 transition-opacity hover:opacity-100 opacity-90">
                  <WeatherWidget weather={weather} location="Lambeau Field" />
                </div>

                {/* Coaching Overlay */}
                <div className="absolute top-4 left-4 z-10 transition-opacity hover:opacity-100 opacity-90">
                  <CoachingWidget teamId={1} />
                </div>

                {/* Crowd Noise Decibel Meter */}
                <div className="absolute top-24 right-4 z-10 transition-opacity hover:opacity-100 opacity-90 scale-90 origin-top-right">
                  <CrowdNoiseMeter
                    decibels={96 + (Number(gameState.homeMomentum) || 0) * 3}
                    stadiumName="Lambeau Field"
                    isAwayTeamOnOffense={true}
                  />
                </div>

                {/* Tactical Kickoff & Simulation Controls Overlay */}
                <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-3 z-20">
                  {!isLive ? (
                    <button
                      onClick={handleStartSimulation}
                      disabled={isLoading}
                      className="flex items-center gap-3 px-8 py-3 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-black font-header text-xl uppercase tracking-widest rounded-full transition-all shadow-[0_0_25px_rgba(16,185,129,0.5)] hover:scale-105"
                    >
                      <Play className="w-5 h-5 fill-black" />
                      {isLoading ? "Starting..." : "KICKOFF"}
                    </button>
                  ) : (
                    <>
                      <button
                        onClick={handleStopSimulation}
                        className="p-3.5 bg-red-600 hover:bg-red-500 text-white rounded-full backdrop-blur-md transition-all shadow-xl hover:scale-105"
                        aria-label="Pause Simulation"
                        title="Pause Simulation"
                      >
                        <Pause className="w-5 h-5" />
                        <span className="sr-only">Pause</span>
                      </button>
                      <button
                        onClick={() => soundEffects.playSnap()}
                        className="p-3.5 bg-white/10 hover:bg-white/20 text-white rounded-full backdrop-blur-md transition-all"
                        aria-label="Fast Forward"
                        title="Fast Forward"
                      >
                        <FastForward className="w-5 h-5" />
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

        {/* Play-by-Play Commentary Feed */}
        <div className="lg:col-span-1 h-full min-h-0 broadcast-glass rounded-2xl border border-white/15 p-2 shadow-2xl">
          <PlayByPlayFeed />
        </div>
      </div>
    </div>
  );
};

export default LiveSim;
