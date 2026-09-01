import React, { useEffect, useState, useCallback } from "react";
import { Canvas } from "@react-three/fiber";
import { motion, AnimatePresence } from "framer-motion";
import { StarfieldBackground } from "../components/skills/StarfieldBackground";
import { DrillSelector } from "../components/training/DrillSelector";
import { CoachingStyleDial } from "../components/training/CoachingStyleDial";
import { WeeklyScheduleTimeline } from "../components/training/WeeklyScheduleTimeline";
import { TrainingSessionResult } from "../components/training/TrainingSessionResult";
import { CampSchedulePlanner } from "../components/training/CampSchedulePlanner";
import { CoachingStylePicker } from "../components/training/CoachingStylePicker";
import { PlayerProgressChart } from "../components/training/PlayerProgressChart";
import { trainingApi } from "../services/trainingApi";
import type { Drill, CoachingStyle, TrainingResult } from "../types/training";
import { CoachingStyleType } from "../types/training";
import { ChevronLeft, User, AlertTriangle } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";

// Types for player data
interface PlayerWeaknessData {
  player_id: number;
  player_name: string;
  position: string;
  age: number;
  weaknesses: string[];
  fatigue: number;
}

export const TrainingCenter: React.FC = () => {
  const { playerId } = useParams<{ playerId?: string }>();

  const [styles, setStyles] = useState<CoachingStyle[]>([]);
  const [selectedDrill, setSelectedDrill] = useState<Drill | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>("smart");
  const [loading, setLoading] = useState(true);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingResult, setTrainingResult] = useState<TrainingResult | null>(null);

  // Player-specific data
  const [playerData, setPlayerData] = useState<PlayerWeaknessData | null>(null);
  const [playerWeaknesses, setPlayerWeaknesses] = useState<string[]>([]);

  // Fetch coaching styles and player data on mount
  useEffect(() => {
    async function init() {
      try {
        const styleData = await trainingApi.getCoachingStyles();
        setStyles(styleData);

        // Fetch player weaknesses if playerId is provided
        if (playerId) {
          try {
            const response = await axios.get(
              `http://localhost:8000/api/v1/players/${playerId}/training-profile`
            );
            setPlayerData(response.data);
            setPlayerWeaknesses(response.data.weaknesses || []);
          } catch (playerErr) {
            console.warn("Could not fetch player training profile, using defaults", playerErr);
            // Default weaknesses for demo
            setPlayerWeaknesses(["route_running", "catching"]);
          }
        } else {
          // Default demo weaknesses when no player selected
          setPlayerWeaknesses(["speed", "awareness"]);
        }
      } catch (err) {
        console.error("Failed to load training data", err);
      } finally {
        setLoading(false);
      }
    }
    init();
  }, [playerId]);

  const handleDrillSelect = useCallback((drill: Drill) => {
    setSelectedDrill((prev) => (prev?.name === drill.name ? null : drill));
  }, []);

  const handleTrain = async () => {
    if (!selectedDrill) return;

    setIsTraining(true);
    try {
      const result = await trainingApi.executeTraining(
        playerData?.player_id || 1,
        selectedDrill.name,
        selectedStyle,
        "regular",
        playerData?.age || 25
      );
      setTrainingResult(result);
    } catch (err) {
      console.error("Training failed", err);
      alert("Training session failed. Please try again.");
    } finally {
      setIsTraining(false);
    }
  };

  const handleResultClose = () => {
    setTrainingResult(null);
    setSelectedDrill(null);
  };

  return (
    <div className="relative w-full min-h-screen overflow-hidden bg-black font-sans text-white">
      {/* 3D Background */}
      <div className="absolute inset-0 z-0 opacity-60">
        <Canvas camera={{ position: [0, 0, 20], fov: 45 }}>
          <ambientLight intensity={0.5} />
          <StarfieldBackground />
        </Canvas>
      </div>

      {/* UI Overlay */}
      <div className="relative z-10 w-full min-h-screen overflow-y-auto custom-scrollbar">
        <div className="container mx-auto px-6 py-8">
          {/* Header */}
          <motion.header
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="flex items-center justify-between mb-12"
          >
            <div className="flex items-center gap-4">
              <Link to="/season" className="p-2 rounded-full hover:bg-white/10 transition-colors">
                <ChevronLeft className="w-6 h-6" />
              </Link>
              <div>
                <h1 className="text-4xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-200">
                  TRAINING CENTER
                </h1>
                <p className="text-gray-400 text-sm tracking-widest uppercase mt-1">
                  Digital Field Operations // Season Phase: Regular
                </p>
              </div>
            </div>

            {/* Player Info & Stats */}
            <div className="flex gap-8 items-center">
              {playerData && (
                <div className="flex items-center gap-3 bg-gray-800/50 px-4 py-2 rounded-xl border border-gray-700/50">
                  <User className="w-5 h-5 text-blue-400" />
                  <div>
                    <div className="text-sm font-bold text-white">{playerData.player_name}</div>
                    <div className="text-xs text-gray-500">
                      {playerData.position} • Age {playerData.age}
                    </div>
                  </div>
                </div>
              )}

              <div className="text-right">
                <div className="text-2xl font-bold text-white">
                  {playerData ? `${100 - playerData.fatigue}%` : "94%"}
                </div>
                <div className="text-xs text-gray-500 uppercase">Energy</div>
              </div>
              <div className="text-right">
                <div
                  className={`text-2xl font-bold ${(playerData?.fatigue ?? 0) > 70 ? "text-red-400" : "text-green-400"}`}
                >
                  {(playerData?.fatigue ?? 0) > 70 ? "High" : "Low"}
                </div>
                <div className="text-xs text-gray-500 uppercase">Injury Risk</div>
              </div>
            </div>
          </motion.header>

          {/* Coaching Dial & Schedule */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-8">
            <motion.section
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="xl:col-span-1"
            >
              <CoachingStyleDial
                styles={styles}
                selectedStyle={selectedStyle}
                onSelect={setSelectedStyle}
              />
            </motion.section>

            <motion.section
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="xl:col-span-2 flex items-center"
            >
              <WeeklyScheduleTimeline selectedDay="MON" onSelectDay={() => {}} />
            </motion.section>
          </div>

          {/* Coaching Style Philosophy Picker */}
          <div className="mb-12">
            <h3 className="text-xs font-mono uppercase tracking-wider text-gray-400 mb-3">
              Coaching Philosophy Matrix
            </h3>
            <CoachingStylePicker
              currentStyle={
                Object.values(CoachingStyleType).includes(selectedStyle as CoachingStyleType)
                  ? (selectedStyle as CoachingStyleType)
                  : CoachingStyleType.SMART
              }
              onStyleSelect={(style) => setSelectedStyle(style)}
            />
          </div>

          {/* Tactical 7-Day Camp Planner */}
          <div className="mb-16">
            <CampSchedulePlanner />
          </div>

          {/* Main Content - DrillSelector */}
          <main>
            {loading ? (
              <div className="text-center py-20 text-gray-500 animate-pulse">
                Initializing Sim...
              </div>
            ) : (
              <DrillSelector
                position={playerData?.position}
                onDrillSelect={handleDrillSelect}
                selectedDrill={selectedDrill}
                playerWeaknesses={playerWeaknesses}
              />
            )}
          </main>

          {/* Player Attribute Progression Trajectory */}
          <div className="mt-12 bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-2xl">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4">
              Player Attribute Progression Trajectory
            </h3>
            <PlayerProgressChart
              playerId={playerData?.player_id ?? 1}
              playerName={playerData?.player_name ?? "Joe Burrow"}
              position={playerData?.position ?? "QB"}
              stats={[
                { stat: "Speed", current: 88, previous: 85, max: 99, color: "#fbbf24" },
                { stat: "Throwing", current: 94, previous: 92, max: 99, color: "#06b6d4" },
                { stat: "Awareness", current: 95, previous: 90, max: 99, color: "#a855f7" },
                { stat: "Stamina", current: 92, previous: 92, max: 99, color: "#3b82f6" },
              ]}
              weeklyXP={[120, 180, 240, 210, 320]}
            />
          </div>
        </div>
      </div>

      {/* Action Shade / Modal for Selected Drill */}
      <AnimatePresence>
        {selectedDrill && !trainingResult && (
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            className="fixed bottom-0 left-0 w-full bg-gray-900 border-t border-blue-500/50 z-50 shadow-[0_-10px_40px_rgba(0,0,0,0.8)]"
          >
            <div className="container mx-auto px-6 py-8 flex flex-wrap items-center justify-between gap-6">
              <div className="max-w-2xl">
                <h2 className="text-3xl font-bold mb-2 text-white">{selectedDrill.name}</h2>
                <div className="text-blue-400 font-mono text-sm mb-4">
                  {selectedDrill.target_stat} Target Protocol
                </div>
                <p className="text-gray-300 leading-relaxed">{selectedDrill.description}</p>

                {/* Injury Risk Warning */}
                {selectedDrill.injury_risk > 0.08 && (
                  <div className="mt-4 flex items-center gap-2 text-red-400 text-sm">
                    <AlertTriangle className="w-4 h-4" />
                    High-intensity drill. Increased injury risk.
                  </div>
                )}
              </div>

              <div className="flex gap-6 items-center">
                <div className="text-right">
                  <div className="text-sm text-gray-400">Estimated XP</div>
                  <div className="text-4xl font-bold text-green-400">
                    +{Math.round(100 * selectedDrill.xp_multiplier)}
                  </div>
                </div>
                <button
                  onClick={() => setSelectedDrill(null)}
                  className="px-6 py-4 bg-gray-700 hover:bg-gray-600 text-white font-bold tracking-widest uppercase rounded transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handleTrain}
                  disabled={isTraining}
                  className={`px-12 py-4 font-bold tracking-widest uppercase rounded shadow-lg transition-all transform hover:scale-105 ${
                    isTraining
                      ? "bg-gray-600 cursor-not-allowed"
                      : "bg-blue-600 hover:bg-blue-500 text-white hover:shadow-blue-500/25"
                  }`}
                >
                  {isTraining ? "Training..." : "Initiate Sequence"}
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Training Result Modal */}
      {trainingResult && (
        <TrainingSessionResult result={trainingResult} onClose={handleResultClose} />
      )}
    </div>
  );
};
