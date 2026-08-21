import React from "react";
import { BatteryCharging, Flame, Brain, HeartPulse, Wind } from "lucide-react";
import type { FatigueState } from "../../types/medical";

interface FatigueMonitorProps {
  fatigue?: FatigueState | null;
  currentWearLevel?: number;
}

export const FatigueMonitor: React.FC<FatigueMonitorProps> = ({
  fatigue,
  currentWearLevel = 15,
}) => {
  // Defaults based on the 4-compartment biological model
  const atp = fatigue?.atp_pc ?? 92; // 0-100%
  const glycolytic = fatigue?.glycolytic ?? 85; // 0-100%
  const aerobic = fatigue?.aerobic ?? 96; // 0-100%
  const neural = fatigue?.neural ?? 88; // 0-100%
  const hrv = fatigue?.hrv ?? 74; // ms
  const lacticAcid = fatigue?.lactic_acid ?? 1.8; // mmol/L
  const homeClimate = fatigue?.home_climate ?? "Temperate";

  const getCompartmentColor = (val: number) => {
    if (val >= 80) return "from-emerald-500 to-teal-400";
    if (val >= 60) return "from-cyan-500 to-blue-400";
    if (val >= 40) return "from-amber-500 to-orange-400";
    return "from-rose-600 to-red-500";
  };

  return (
    <div className="w-full rounded-2xl bg-slate-950/80 border border-slate-800 p-5 shadow-2xl backdrop-blur-xl font-sans">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/30 text-indigo-400">
            <HeartPulse className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white tracking-wide uppercase">
              4-Compartment Biological Bio-Monitor
            </h3>
            <p className="text-[11px] text-slate-400 font-mono">
              Cellular ATP • Lactate Threshold • Neural Latency
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 font-mono text-xs">
          <span className="text-slate-400">HRV:</span>
          <span className="text-emerald-400 font-bold px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-800/40">
            {hrv} ms (Optimal)
          </span>
        </div>
      </div>

      {/* 4 Energy Compartment Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 1. ATP-PC Reservoir */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl">
          <div className="flex justify-between items-center text-xs mb-1.5">
            <span className="font-semibold text-slate-200 flex items-center gap-1.5">
              <BatteryCharging className="w-3.5 h-3.5 text-cyan-400" /> ATP-PC Burst Reservoir
            </span>
            <span className="font-mono font-bold text-cyan-300">{Math.round(atp)}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full bg-gradient-to-r ${getCompartmentColor(atp)}`}
              style={{ width: `${atp}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>Fast recovery (0.3/tick)</span>
            <span>Explosive snap readiness</span>
          </div>
        </div>

        {/* 2. Glycolytic / Lactate System */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl">
          <div className="flex justify-between items-center text-xs mb-1.5">
            <span className="font-semibold text-slate-200 flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-amber-400" /> Glycolytic System
            </span>
            <span className="font-mono font-bold text-amber-300">{Math.round(glycolytic)}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full bg-gradient-to-r ${getCompartmentColor(glycolytic)}`}
              style={{ width: `${glycolytic}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>Lactate: {lacticAcid} mmol/L</span>
            <span>Medium-burn threshold</span>
          </div>
        </div>

        {/* 3. Aerobic Base */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl">
          <div className="flex justify-between items-center text-xs mb-1.5">
            <span className="font-semibold text-slate-200 flex items-center gap-1.5">
              <Wind className="w-3.5 h-3.5 text-emerald-400" /> Aerobic Foundation
            </span>
            <span className="font-mono font-bold text-emerald-300">{Math.round(aerobic)}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full bg-gradient-to-r ${getCompartmentColor(aerobic)}`}
              style={{ width: `${aerobic}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>Base endurance (500 capacity)</span>
            <span>Climate: {homeClimate}</span>
          </div>
        </div>

        {/* 4. Neural / Reaction System */}
        <div className="bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl">
          <div className="flex justify-between items-center text-xs mb-1.5">
            <span className="font-semibold text-slate-200 flex items-center gap-1.5">
              <Brain className="w-3.5 h-3.5 text-indigo-400" /> Neural & Decision Sharpness
            </span>
            <span className="font-mono font-bold text-indigo-300">{Math.round(neural)}%</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full bg-gradient-to-r ${getCompartmentColor(neural)}`}
              style={{ width: `${neural}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>Pre-snap read latency: 0ms</span>
            <span>Mental fatigue index</span>
          </div>
        </div>
      </div>

      {/* Micro-wear Summary */}
      <div className="mt-3 pt-3 border-t border-slate-800/60 flex items-center justify-between text-xs font-mono text-slate-400">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          <span>
            Active Game Wear Accumulation:{" "}
            <strong className="text-white">{currentWearLevel}%</strong>
          </span>
        </div>
        <span className="text-[11px] text-slate-500">Recovers weekly during rest days</span>
      </div>
    </div>
  );
};
