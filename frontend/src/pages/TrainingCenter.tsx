import { useEffect, useState } from "react";
import type { Drill } from "../types/training";
import { CoachingStyleType } from "../types/training";
import { trainingService } from "../services/trainingApi";
import { DrillCard } from "../components/training/DrillCard";
import { CoachingStylePicker } from "../components/training/CoachingStylePicker";
import { CoachCard } from "../components/coaching/CoachCard";
import { Loader2 } from "lucide-react";
import "../components/training/TrainingCenter.css";

export const TrainingCenter = () => {
  const [loading, setLoading] = useState(true);
  const [drills, setDrills] = useState<Drill[]>([]);
  const [currentStyle, setCurrentStyle] = useState<CoachingStyleType>(CoachingStyleType.SMART);
  const [selectedDrills, setSelectedDrills] = useState<string[]>([]);

  // Mock coach data - in production, fetch from API
  const headCoach = {
    name: "Andy Reid",
    role: "Head Coach",
    tier: "LEGEND",
    archetype: "QB_GURU",
    playbookOffense: "West Coast",
    experience: 26,
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [drillsData, scheduleData] = await Promise.all([
          trainingService.getDrills(),
          trainingService.getSchedule(),
        ]);
        setDrills(drillsData);
        setCurrentStyle(scheduleData.coachingStyle);
      } catch (err) {
        console.error("Failed to load training data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleStyleChange = async (style: CoachingStyleType) => {
    setCurrentStyle(style);
    await trainingService.setCoachingStyle(style);
  };

  const handleDrillToggle = (drill: Drill) => {
    setSelectedDrills((prev) =>
      prev.includes(drill.id) ? prev.filter((id) => id !== drill.id) : [...prev, drill.id]
    );
  };

  const handleExecute = async () => {
    setLoading(true);
    await trainingService.executeTraining();
    setLoading(false);
    // TODO: Show success notification or summary
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col gap-6 p-6 overflow-y-auto">
      {/* Header */}
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Training Center</h1>
          <p className="text-cyan-400/80 text-sm">Week 4 Prep • OVR Team Energy: 88%</p>
        </div>
        <button
          onClick={handleExecute}
          className="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-black font-bold rounded-lg transition-colors shadow-lg shadow-emerald-500/20"
        >
          Execute Week
        </button>
      </header>

      {/* Coaching Staff */}
      <section>
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-1 h-6 bg-purple-400 rounded-full" />
          Head Coach
        </h2>
        <CoachCard {...headCoach} />
      </section>

      {/* Coaching Philosophy */}
      <section>
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-1 h-6 bg-cyan-400 rounded-full" />
          Coaching Philosophy
        </h2>
        <CoachingStylePicker currentStyle={currentStyle} onStyleSelect={handleStyleChange} />
      </section>

      {/* Drill Catalog */}
      <section className="flex-1">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-1 h-6 bg-amber-400 rounded-full" />
          Drill Catalog
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {drills.map((drill) => (
            <DrillCard
              key={drill.id}
              drill={drill}
              isSelected={selectedDrills.includes(drill.id)}
              onSelect={handleDrillToggle}
            />
          ))}
        </div>
      </section>
    </div>
  );
};
