import { useEffect, useState } from "react";
import type { Drill } from "../types/training";
import { CoachingStyleType } from "../types/training";
import { trainingService } from "../services/trainingApi";
import type { BatchExecuteRequest } from "../services/trainingApi";
import { useNotificationStore } from "../store/useNotificationStore";
import { DrillCard } from "../components/training/DrillCard";
import { CoachingStylePicker } from "../components/training/CoachingStylePicker";
import { Loader2 } from "lucide-react";
import "../components/training/TrainingCenter.css";

export const TrainingCenter = () => {
  const [loading, setLoading] = useState(true);
  const [drills, setDrills] = useState<Drill[]>([]);
  const [currentStyle, setCurrentStyle] = useState<CoachingStyleType>(CoachingStyleType.SMART);
  const [selectedDrills, setSelectedDrills] = useState<string[]>([]);
  const addNotification = useNotificationStore((state) => state.addNotification);

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

    // Construct a mock batch request for now based on selected drills
    // In a real app, this would use actual player IDs and scheduled assignments
    const request: BatchExecuteRequest = {
      assignments: selectedDrills.map((drillId) => ({
        player_id: Math.floor(Math.random() * 50) + 1, // Mock Player IDs
        drill_name: drills.find((d) => d.id === drillId)?.name || "Unknown Drill",
        season_phase: "regular",
        player_age: 22,
        coaching_style: currentStyle,
      })),
    };

    // If no drills selected, add at least one dummy one to show the flow
    if (request.assignments.length === 0) {
      request.assignments.push({
        player_id: 12,
        drill_name: "7-on-7 Skeleton",
        season_phase: "regular",
        player_age: 22,
        coaching_style: currentStyle,
      });
    }

    try {
      const result = await trainingService.executeBatchTraining(request);
      addNotification({
        type: "TRAINING_SUMMARY",
        data: result,
        duration: 5000,
      });
    } catch (error) {
      console.error("Training failed:", error);
    } finally {
      setLoading(false);
    }
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
