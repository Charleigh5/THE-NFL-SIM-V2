import React, { useEffect, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { motion, AnimatePresence } from "framer-motion";
import { StarfieldBackground } from "../components/skills/StarfieldBackground";
import { DrillCard3D } from "../components/training/DrillCard3D";
import { CoachingStyleDial } from "../components/training/CoachingStyleDial";
import { WeeklyScheduleTimeline } from "../components/training/WeeklyScheduleTimeline";
import { trainingApi } from "../services/trainingApi";
import type { Drill, CoachingStyle } from "../types/training";
import { SeasonPhase } from "../types/training";
import { ChevronLeft } from "lucide-react";
import { Link } from "react-router-dom";

export const TrainingCenter: React.FC = () => {
  const [drills, setDrills] = useState<Drill[]>([]);
  const [styles, setStyles] = useState<CoachingStyle[]>([]);
  const [selectedDrill, setSelectedDrill] = useState<Drill | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string>("smart");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function init() {
      try {
        const [drillData, styleData] = await Promise.all([
          trainingApi.getDrills({ season: SeasonPhase.REGULAR }),
          trainingApi.getCoachingStyles(),
        ]);
        setDrills(drillData.drills);
        setStyles(styleData);
      } catch (err) {
        console.error("Failed to load training data", err);
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  const handleTrain = async () => {
    if (!selectedDrill) return;
    // TODO: Connect to real player ID context
    const result = await trainingApi.executeTraining(1, selectedDrill.name, selectedStyle);
    alert(`Training Complete! XP Gained: ${result.xp_gained}`);
    setSelectedDrill(null);
  };

  return (
    <div className="relative w-full h-screen overflow-hidden bg-black font-sans text-white">
      {/* 3D Background */}
      <div className="absolute inset-0 z-0 opacity-60">
        <Canvas camera={{ position: [0, 0, 20], fov: 45 }}>
          <ambientLight intensity={0.5} />
          <StarfieldBackground />
        </Canvas>
      </div>

      {/* UI Overlay */}
      <div className="relative z-10 w-full h-full overflow-y-auto custom-scrollbar">
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

            {/* Stats Summary (Mock) */}
            <div className="flex gap-8 text-right">
              <div>
                <div className="text-2xl font-bold text-white">94%</div>
                <div className="text-xs text-gray-500 uppercase">Team Energy</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-400">Low</div>
                <div className="text-xs text-gray-500 uppercase">Injury Risk</div>
              </div>
            </div>
          </motion.header>

          {/* Coaching Dial & Schedule */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-16">
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

          {/* Main Content Grid */}
          <main className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Drill Filters / Sidebar (Future) */}
            <div className="hidden lg:block lg:col-span-1 space-y-4">
              <h3 className="text-lg font-bold border-b border-white/20 pb-2">CATEGORIES</h3>
              {["QB Skill", "Strength", "Film Study", "Recovery"].map((cat) => (
                <div
                  key={cat}
                  className="p-3 rounded bg-white/5 hover:bg-white/10 cursor-pointer text-sm"
                >
                  {cat}
                </div>
              ))}
            </div>

            {/* Drill Catalogue */}
            <div className="lg:col-span-3">
              <h3 className="text-lg font-bold border-b border-white/20 pb-2 mb-6 text-right">
                AVAILABLE PROTOCOLS
              </h3>

              {loading ? (
                <div className="text-center py-20 text-gray-500 animate-pulse">
                  Initializing Sim...
                </div>
              ) : (
                <motion.div
                  layout
                  className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 justify-items-center"
                >
                  {drills.map((drill) => (
                    <DrillCard3D
                      key={drill.name}
                      drill={drill}
                      isSelected={selectedDrill?.name === drill.name}
                      onSelect={setSelectedDrill}
                    />
                  ))}
                </motion.div>
              )}
            </div>
          </main>
        </div>
      </div>

      {/* Action Shade / Modal */}
      <AnimatePresence>
        {selectedDrill && (
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            className="fixed bottom-0 left-0 w-full h-80 bg-gray-900 border-t border-blue-500/50 z-50 shadow-[0_-10px_40px_rgba(0,0,0,0.8)]"
          >
            <div className="container mx-auto px-6 py-8 flex items-center justify-between h-full">
              <div className="max-w-2xl">
                <h2 className="text-3xl font-bold mb-2 text-white">{selectedDrill.name}</h2>
                <div className="text-blue-400 font-mono text-sm mb-4">
                  {selectedDrill.target_stat} Target Protocol
                </div>
                <p className="text-gray-300 leading-relaxed">{selectedDrill.description}</p>
              </div>

              <div className="flex gap-6 items-center">
                <div className="text-right">
                  <div className="text-sm text-gray-400">Estimated XP</div>
                  <div className="text-4xl font-bold text-green-400">
                    +{Math.round(100 * selectedDrill.xp_multiplier)}
                  </div>
                </div>
                <button
                  onClick={handleTrain}
                  className="px-12 py-6 bg-blue-600 hover:bg-blue-500 text-white font-bold tracking-widest uppercase rounded shadow-lg hover:shadow-blue-500/25 transition-all transform hover:scale-105"
                >
                  Initiate Sequence
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
