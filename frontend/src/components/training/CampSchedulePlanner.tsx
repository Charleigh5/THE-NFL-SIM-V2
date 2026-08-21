import React, { useState } from "react";
import { Calendar, Sun, Moon, Battery } from "lucide-react";

export type IntensityLevel = "WALKTHROUGH" | "STANDARD" | "FULL_PADS";
export type CampDrillType =
  | "OKLAHOMA"
  | "7_ON_7"
  | "INDIVIDUAL"
  | "FILM_STUDY"
  | "SCRIMMAGE"
  | "CONDITIONING";

export interface DaySchedule {
  dayNumber: number;
  dayName: string;
  focusTitle: string;
  isRestDay: boolean;
  intensity: IntensityLevel;
  morningDrill: CampDrillType;
  afternoonDrill: CampDrillType;
}

interface CampSchedulePlannerProps {
  onScheduleChange?: (schedule: DaySchedule[]) => void;
  onSimulateCampWeek?: () => void;
}

export const CampSchedulePlanner: React.FC<CampSchedulePlannerProps> = ({
  onScheduleChange,
  onSimulateCampWeek,
}) => {
  const drillSpecs: Record<
    CampDrillType,
    { name: string; target: string; xp: number; injury: number; fatigue: number }
  > = {
    OKLAHOMA: {
      name: "Oklahoma Drill",
      target: "Strength & Tackling",
      xp: 1.5,
      injury: 5.0,
      fatigue: 15.0,
    },
    "7_ON_7": {
      name: "7-on-7 Passing",
      target: "Passing & Coverage",
      xp: 1.2,
      injury: 2.0,
      fatigue: 10.0,
    },
    INDIVIDUAL: {
      name: "Individual Technique",
      target: "Position Skills",
      xp: 1.0,
      injury: 1.0,
      fatigue: 5.0,
    },
    FILM_STUDY: {
      name: "Film Study",
      target: "Awareness & Play Rec",
      xp: 0.8,
      injury: 0.0,
      fatigue: 0.0,
    },
    SCRIMMAGE: {
      name: "Full Scrimmage",
      target: "Full Team Execution",
      xp: 2.0,
      injury: 8.0,
      fatigue: 25.0,
    },
    CONDITIONING: {
      name: "Conditioning Gassers",
      target: "Stamina & Speed",
      xp: 0.9,
      injury: 3.0,
      fatigue: 20.0,
    },
  };

  const intensityMultipliers: Record<IntensityLevel, number> = {
    WALKTHROUGH: 0.5,
    STANDARD: 1.0,
    FULL_PADS: 1.5,
  };

  // Recommended standard 7-day schedule from camp.py and master dossier
  const [schedule, setSchedule] = useState<DaySchedule[]>([
    {
      dayNumber: 1,
      dayName: "Mon",
      focusTitle: "Acclimation & Stems",
      isRestDay: false,
      intensity: "STANDARD",
      morningDrill: "INDIVIDUAL",
      afternoonDrill: "7_ON_7",
    },
    {
      dayNumber: 2,
      dayName: "Tue",
      focusTitle: "Scheme Install",
      isRestDay: false,
      intensity: "STANDARD",
      morningDrill: "FILM_STUDY",
      afternoonDrill: "INDIVIDUAL",
    },
    {
      dayNumber: 3,
      dayName: "Wed",
      focusTitle: "Heavy Contact Day",
      isRestDay: false,
      intensity: "FULL_PADS",
      morningDrill: "OKLAHOMA",
      afternoonDrill: "SCRIMMAGE",
    },
    {
      dayNumber: 4,
      dayName: "Thu",
      focusTitle: "Mental Recovery",
      isRestDay: false,
      intensity: "WALKTHROUGH",
      morningDrill: "FILM_STUDY",
      afternoonDrill: "FILM_STUDY",
    },
    {
      dayNumber: 5,
      dayName: "Fri",
      focusTitle: "Red Zone Specifics",
      isRestDay: false,
      intensity: "STANDARD",
      morningDrill: "INDIVIDUAL",
      afternoonDrill: "7_ON_7",
    },
    {
      dayNumber: 6,
      dayName: "Sat",
      focusTitle: "Game Simulation",
      isRestDay: false,
      intensity: "FULL_PADS",
      morningDrill: "SCRIMMAGE",
      afternoonDrill: "CONDITIONING",
    },
    {
      dayNumber: 7,
      dayName: "Sun",
      focusTitle: "Active Recovery",
      isRestDay: true,
      intensity: "WALKTHROUGH",
      morningDrill: "FILM_STUDY",
      afternoonDrill: "FILM_STUDY",
    },
  ]);

  const [selectedDayIdx, setSelectedDayIdx] = useState<number>(0);

  // Calculations for weekly yields
  const calculateTotals = () => {
    let totalXp = 0;
    let totalFatigue = 0;
    let maxInjuryRisk = 0;

    schedule.forEach((day) => {
      if (day.isRestDay) {
        totalFatigue = Math.max(0, totalFatigue - 20.0);
      } else {
        const intMod = intensityMultipliers[day.intensity];
        const mXp = drillSpecs[day.morningDrill].xp * 10.0 * intMod;
        const aXp = drillSpecs[day.afternoonDrill].xp * 10.0 * intMod;
        totalXp += mXp + aXp;

        const mFatigue = drillSpecs[day.morningDrill].fatigue * intMod;
        const aFatigue = drillSpecs[day.afternoonDrill].fatigue * intMod;
        totalFatigue += mFatigue + aFatigue;

        const dayRisk =
          (drillSpecs[day.morningDrill].injury + drillSpecs[day.afternoonDrill].injury) * intMod;
        if (dayRisk > maxInjuryRisk) maxInjuryRisk = dayRisk;
      }
    });

    return {
      projectedXp: Math.round(totalXp),
      netFatigue: Math.round(totalFatigue),
      peakInjuryRisk: Math.round(maxInjuryRisk),
    };
  };

  const totals = calculateTotals();
  const activeDay = schedule[selectedDayIdx];

  const updateActiveDay = (updates: Partial<DaySchedule>) => {
    const updated = schedule.map((d, idx) => (idx === selectedDayIdx ? { ...d, ...updates } : d));
    setSchedule(updated);
    if (onScheduleChange) onScheduleChange(updated);
  };

  return (
    <div className="w-full bg-slate-950/90 border border-slate-800 rounded-2xl p-6 shadow-2xl backdrop-blur-xl font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800 mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Calendar className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-wide uppercase flex items-center gap-2">
              Tactical 7-Day Camp Planner
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                PRO SCHEDULE
              </span>
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Morning & Afternoon Drill Slots • Rest Recovery • Load Management
            </p>
          </div>
        </div>

        {/* Weekly Metrics Banner */}
        <div className="flex items-center gap-4 bg-slate-900 border border-slate-800 px-4 py-2 rounded-xl text-xs font-mono">
          <div>
            <span className="text-slate-400 block text-[10px]">Projected XP</span>
            <span className="text-emerald-400 font-bold text-sm">+{totals.projectedXp} XP</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-slate-400 block text-[10px]">Net Fatigue</span>
            <span className="text-amber-400 font-bold text-sm">+{totals.netFatigue}%</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-slate-400 block text-[10px]">Peak Hazard</span>
            <span
              className={`font-bold text-sm ${
                totals.peakInjuryRisk > 10 ? "text-red-400" : "text-cyan-400"
              }`}
            >
              {totals.peakInjuryRisk}%
            </span>
          </div>
        </div>
      </div>

      {/* 7-Day Selector Bar */}
      <div className="grid grid-cols-7 gap-2 mb-6">
        {schedule.map((day, idx) => (
          <button
            key={day.dayNumber}
            onClick={() => setSelectedDayIdx(idx)}
            className={`p-3 rounded-xl border text-center transition-all ${
              selectedDayIdx === idx
                ? "bg-cyan-950 border-cyan-500 text-white shadow-lg shadow-cyan-950/60"
                : day.isRestDay
                  ? "bg-slate-900/40 border-slate-800 text-emerald-400"
                  : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            <div className="text-[10px] font-mono uppercase text-slate-400">{day.dayName}</div>
            <div className="text-sm font-bold my-0.5">Day {day.dayNumber}</div>
            <div
              className={`text-[9px] font-mono px-1 py-0.5 rounded truncate ${
                day.isRestDay
                  ? "bg-emerald-950 text-emerald-300"
                  : day.intensity === "FULL_PADS"
                    ? "bg-red-950 text-red-300"
                    : "bg-slate-800 text-slate-300"
              }`}
            >
              {day.isRestDay ? "REST" : day.intensity}
            </div>
          </button>
        ))}
      </div>

      {/* Active Day Detail Matrix */}
      <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-slate-800/80">
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider">
              {activeDay.dayName} (Day {activeDay.dayNumber}): {activeDay.focusTitle}
            </h4>
            <p className="text-xs text-slate-400">
              Configure morning and afternoon practice blocks.
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Rest Day Toggle */}
            <button
              onClick={() => updateActiveDay({ isRestDay: !activeDay.isRestDay })}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold uppercase transition-all ${
                activeDay.isRestDay
                  ? "bg-emerald-600 text-white shadow-md shadow-emerald-950"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              <Battery className="w-3.5 h-3.5" />
              {activeDay.isRestDay ? "Rest Day Active (-20 Fatigue)" : "Mark as Rest Day"}
            </button>

            {/* Intensity Selector */}
            {!activeDay.isRestDay && (
              <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs font-mono">
                {(["WALKTHROUGH", "STANDARD", "FULL_PADS"] as IntensityLevel[]).map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => updateActiveDay({ intensity: lvl })}
                    className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all ${
                      activeDay.intensity === lvl
                        ? "bg-cyan-600 text-white"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Drill Configuration Slots */}
        {!activeDay.isRestDay ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Morning Slot */}
            <div className="bg-slate-950/80 border border-slate-800 p-4 rounded-xl">
              <div className="flex items-center justify-between mb-3 text-xs">
                <span className="font-bold text-slate-200 flex items-center gap-1.5 font-mono">
                  <Sun className="w-4 h-4 text-amber-400" /> Morning Block
                </span>
                <span className="text-[10px] font-mono text-cyan-400">
                  Target: {drillSpecs[activeDay.morningDrill].target}
                </span>
              </div>
              <select
                value={activeDay.morningDrill}
                onChange={(e) => updateActiveDay({ morningDrill: e.target.value as CampDrillType })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-white font-medium focus:border-cyan-500 focus:outline-none"
              >
                {Object.entries(drillSpecs).map(([key, spec]) => (
                  <option key={key} value={key}>
                    {spec.name} ({spec.xp}x XP, {spec.injury}% Risk, +{spec.fatigue} Fatigue)
                  </option>
                ))}
              </select>
            </div>

            {/* Afternoon Slot */}
            <div className="bg-slate-950/80 border border-slate-800 p-4 rounded-xl">
              <div className="flex items-center justify-between mb-3 text-xs">
                <span className="font-bold text-slate-200 flex items-center gap-1.5 font-mono">
                  <Moon className="w-4 h-4 text-indigo-400" /> Afternoon Block
                </span>
                <span className="text-[10px] font-mono text-cyan-400">
                  Target: {drillSpecs[activeDay.afternoonDrill].target}
                </span>
              </div>
              <select
                value={activeDay.afternoonDrill}
                onChange={(e) =>
                  updateActiveDay({ afternoonDrill: e.target.value as CampDrillType })
                }
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-white font-medium focus:border-cyan-500 focus:outline-none"
              >
                {Object.entries(drillSpecs).map(([key, spec]) => (
                  <option key={key} value={key}>
                    {spec.name} ({spec.xp}x XP, {spec.injury}% Risk, +{spec.fatigue} Fatigue)
                  </option>
                ))}
              </select>
            </div>
          </div>
        ) : (
          <div className="p-8 text-center bg-slate-950/40 rounded-xl border border-dashed border-slate-800">
            <Battery className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            <h5 className="text-sm font-bold text-white mb-1">Scheduled Rest & Hydration Day</h5>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              No on-field contact drills. Roster energy recovers by +20%, eliminating acute
              micro-wear accumulation before next week.
            </p>
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="mt-5 pt-4 border-t border-slate-800 flex justify-end">
        <button
          onClick={onSimulateCampWeek}
          className="px-6 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-lg transition-all"
        >
          Commit Weekly Camp Schedule
        </button>
      </div>
    </div>
  );
};
