import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  TrendingUp,
  Info,
  Calendar,
} from "lucide-react";
import type {
  TreatmentTrajectory,
  MedicalProtocol,
} from "../../types/orthopedicRtp";

interface RTPTrajectoryGraphProps {
  trajectories: TreatmentTrajectory[];
  activeProtocol?: MedicalProtocol;
  onSelectProtocol?: (protocol: MedicalProtocol) => void;
  className?: string;
}

const PROTOCOL_CONFIG: Record<
  MedicalProtocol,
  { name: string; color: string; strokeDash?: string; badgeBg: string }
> = {
  CONSERVATIVE: {
    name: "Conservative Rest",
    color: "#38bdf8", // Sky blue
    badgeBg: "bg-sky-500/20 text-sky-300 border-sky-500/40",
  },
  BIOLOGIC_PRP: {
    name: "Biologic PRP",
    color: "#c084fc", // Purple
    badgeBg: "bg-purple-500/20 text-purple-300 border-purple-500/40",
  },
  ARTHROSCOPIC: {
    name: "Arthroscopic Scope",
    color: "#2dd4bf", // Teal
    badgeBg: "bg-teal-500/20 text-teal-300 border-teal-500/40",
  },
  OPEN_SURGERY: {
    name: "Open Reconstruction",
    color: "#fbbf24", // Amber
    badgeBg: "bg-amber-500/20 text-amber-300 border-amber-500/40",
  },
  CORTISONE: {
    name: "Cortisone Injection",
    color: "#f87171", // Crimson
    strokeDash: "4 3",
    badgeBg: "bg-red-500/20 text-red-300 border-red-500/40",
  },
};

export const RTPTrajectoryGraph: React.FC<RTPTrajectoryGraphProps> = ({
  trajectories,
  activeProtocol = "CONSERVATIVE",
  onSelectProtocol,
  className = "",
}) => {
  // Toggle visible protocols (by default, show all)
  const [visibleProtocols, setVisibleProtocols] = useState<Record<MedicalProtocol, boolean>>({
    CONSERVATIVE: true,
    BIOLOGIC_PRP: true,
    ARTHROSCOPIC: true,
    OPEN_SURGERY: true,
    CORTISONE: true,
  });

  // Hover scrub state (week index 0-12)
  const [hoveredWeek, setHoveredWeek] = useState<number | null>(null);

  const toggleProtocol = (proto: MedicalProtocol) => {
    setVisibleProtocols((prev) => ({
      ...prev,
      [proto]: !prev[proto],
    }));
  };

  // Graph SVG coordinate system
  const width = 640;
  const height = 280;
  const padding = { top: 25, right: 35, bottom: 40, left: 45 };

  const graphWidth = width - padding.left - padding.right;
  const graphHeight = height - padding.top - padding.bottom;

  // Scale functions
  const xScale = (week: number) => padding.left + (week / 12) * graphWidth;
  const yScale = (health: number) => padding.top + graphHeight - (health / 100) * graphHeight;

  // 85% Clearance and 100% Full Strength horizontal reference lines
  const y85 = yScale(85);
  const y100 = yScale(100);

  // Generate SVG path for a trajectory
  const generatePath = (trajectory: TreatmentTrajectory): string => {
    return trajectory.curve.reduce((path, pt, idx) => {
      const x = xScale(pt.week);
      const y = yScale(pt.healthPercentage);
      return idx === 0 ? `M ${x} ${y}` : `${path} L ${x} ${y}`;
    }, "");
  };

  // Find active or highlighted week data
  const scrubWeek = hoveredWeek !== null ? hoveredWeek : 4;

  return (
    <div
      className={`p-5 rounded-3xl bg-slate-950/90 border border-cyan-500/30 shadow-2xl backdrop-blur-md ${className}`}
    >
      {/* Header with Title and Protocol Legend Toggles */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-cyan-950/80 border border-cyan-500/40 text-cyan-400">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px] font-mono uppercase font-bold">
                Gompertz Non-Linear Model
              </span>
              <span className="text-[10px] font-mono text-slate-400">12-Week Projection</span>
            </div>
            <h3 className="text-sm font-bold text-white tracking-wide mt-0.5">
              Orthopedic Return-to-Play (RTP) Trajectory
            </h3>
          </div>
        </div>

        {/* Protocol Visibility Pills */}
        <div className="flex flex-wrap items-center gap-1.5">
          {trajectories.map((traj) => {
            const cfg = PROTOCOL_CONFIG[traj.protocol];
            const isVisible = visibleProtocols[traj.protocol];
            const isSelected = activeProtocol === traj.protocol;

            return (
              <button
                key={traj.protocol}
                onClick={() => {
                  toggleProtocol(traj.protocol);
                  if (onSelectProtocol) onSelectProtocol(traj.protocol);
                }}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-[11px] font-mono font-bold border transition-all ${
                  isVisible
                    ? `${cfg.badgeBg} shadow-sm`
                    : "bg-slate-900/60 text-slate-500 border-slate-800 opacity-60"
                } ${isSelected ? "ring-1 ring-cyan-400" : ""}`}
              >
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: isVisible ? cfg.color : "#64748b" }}
                />
                <span>{cfg.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Scrubbed Week Milestone Status HUD */}
      <div className="mt-3 p-3 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs font-mono">
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-cyan-400" />
          <span className="text-slate-400">Timeline Milestone:</span>
          <span className="text-white font-bold px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800">
            {scrubWeek === 0 ? "Week 0 (Immediate Post-Trauma)" : `Week ${scrubWeek} Post-Treatment`}
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-[11px]">
          {trajectories
            .filter((t) => visibleProtocols[t.protocol])
            .map((t) => {
              const pt = t.curve[scrubWeek] || t.curve[t.curve.length - 1];
              const cfg = PROTOCOL_CONFIG[t.protocol];
              return (
                <div key={t.protocol} className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: cfg.color }} />
                  <span className="text-slate-400">{t.protocol}:</span>
                  <span className="font-bold text-slate-200">{pt.healthPercentage}% Hlt</span>
                  <span className="text-red-400 text-[10px]">({pt.reInjuryRiskPct}% Rsk)</span>
                </div>
              );
            })}
        </div>
      </div>

      {/* SVG Trajectory Chart */}
      <div className="relative mt-3 select-none">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto overflow-visible cursor-crosshair"
          onMouseMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            const relX = e.clientX - rect.left;
            const normX = (relX / rect.width) * width;
            const weekFloat = ((normX - padding.left) / graphWidth) * 12;
            const clampedWeek = Math.max(0, Math.min(12, Math.round(weekFloat)));
            setHoveredWeek(clampedWeek);
          }}
          onMouseLeave={() => setHoveredWeek(null)}
        >
          {/* Horizontal Gridlines & Y-Axis Labels */}
          {[20, 40, 60, 80, 100].map((val) => {
            const y = yScale(val);
            return (
              <g key={val}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="#334155"
                  strokeWidth="1"
                  strokeDasharray="2 4"
                />
                <text
                  x={padding.left - 8}
                  y={y + 3}
                  textAnchor="end"
                  className="text-[10px] fill-slate-500 font-mono"
                >
                  {val}%
                </text>
              </g>
            );
          })}

          {/* 85% Clearance Threshold Line */}
          <line
            x1={padding.left}
            y1={y85}
            x2={width - padding.right}
            y2={y85}
            stroke="#10b981"
            strokeWidth="1.5"
            strokeDasharray="4 4"
            className="opacity-70"
          />
          <text
            x={width - padding.right}
            y={y85 - 5}
            textAnchor="end"
            className="text-[9px] fill-emerald-400 font-mono font-bold"
          >
            85% CLINICALLY CLEARED
          </text>

          {/* 100% Full Strength Threshold Line */}
          <line
            x1={padding.left}
            y1={y100}
            x2={width - padding.right}
            y2={y100}
            stroke="#06b6d4"
            strokeWidth="1.5"
            strokeDasharray="3 3"
            className="opacity-50"
          />
          <text
            x={width - padding.right}
            y={y100 - 5}
            textAnchor="end"
            className="text-[9px] fill-cyan-400 font-mono font-bold"
          >
            100% FULL INTEGRITY
          </text>

          {/* X-Axis Vertical Gridlines & Labels */}
          {Array.from({ length: 13 }).map((_, w) => {
            const x = xScale(w);
            return (
              <g key={w}>
                <line
                  x1={x}
                  y1={padding.top}
                  x2={x}
                  y2={height - padding.bottom}
                  stroke="#1e293b"
                  strokeWidth="1"
                />
                <text
                  x={x}
                  y={height - padding.bottom + 16}
                  textAnchor="middle"
                  className={`text-[10px] font-mono ${
                    scrubWeek === w ? "fill-cyan-400 font-bold" : "fill-slate-500"
                  }`}
                >
                  W{w}
                </text>
              </g>
            );
          })}

          {/* Trajectory Curve Paths */}
          {trajectories.map((traj) => {
            if (!visibleProtocols[traj.protocol]) return null;
            const cfg = PROTOCOL_CONFIG[traj.protocol];
            const pathData = generatePath(traj);

            return (
              <g key={traj.protocol}>
                <motion.path
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{ duration: 0.8, ease: "easeOut" }}
                  d={pathData}
                  fill="none"
                  stroke={cfg.color}
                  strokeWidth={activeProtocol === traj.protocol ? 3 : 2}
                  strokeDasharray={cfg.strokeDash || undefined}
                  className="transition-all"
                />
                {/* Milestone Points */}
                {traj.curve.map((pt) => {
                  const cx = xScale(pt.week);
                  const cy = yScale(pt.healthPercentage);
                  const isScrubbed = scrubWeek === pt.week;
                  return (
                    <circle
                      key={pt.week}
                      cx={cx}
                      cy={cy}
                      r={isScrubbed ? 4.5 : 2.5}
                      fill={cfg.color}
                      className={`transition-all ${
                        isScrubbed ? "stroke-2 stroke-slate-900 shadow-lg" : ""
                      }`}
                    />
                  );
                })}
              </g>
            );
          })}

          {/* Vertical Scrub Cursor Line */}
          {scrubWeek !== null && (
            <line
              x1={xScale(scrubWeek)}
              y1={padding.top}
              x2={xScale(scrubWeek)}
              y2={height - padding.bottom}
              stroke="#00f0ff"
              strokeWidth="1.5"
              strokeDasharray="3 2"
              className="pointer-events-none"
            />
          )}
        </svg>
      </div>

      {/* Protocol Metrics Comparison Table */}
      <div className="mt-4 pt-3 border-t border-slate-800">
        <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
          <Info className="w-3.5 h-3.5 text-cyan-400" />
          Clinical Pathway Metrics & Cost Trade-Offs
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2">
          {trajectories.map((traj) => {
            const cfg = PROTOCOL_CONFIG[traj.protocol];
            const isSelected = activeProtocol === traj.protocol;
            return (
              <div
                key={traj.protocol}
                onClick={() => {
                  if (onSelectProtocol) onSelectProtocol(traj.protocol);
                }}
                className={`p-2.5 rounded-xl border cursor-pointer transition-all ${
                  isSelected
                    ? "bg-cyan-950/50 border-cyan-400"
                    : "bg-slate-900/40 border-slate-800 hover:bg-slate-900/70"
                }`}
              >
                <div className="flex items-center justify-between gap-1 mb-1">
                  <span
                    className="w-2 h-2 rounded-full shrink-0"
                    style={{ backgroundColor: cfg.color }}
                  />
                  <span className="text-[11px] font-bold text-white truncate">{cfg.name}</span>
                </div>
                <div className="text-[10px] font-mono text-slate-400 space-y-0.5">
                  <div className="flex justify-between">
                    <span>Est. Out:</span>
                    <strong className="text-cyan-300">
                      {traj.estRecoveryWeeks === 0 ? "0 Wks" : `~${traj.estRecoveryWeeks} Wks`}
                    </strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Risk:</span>
                    <strong
                      className={
                        traj.complicationRiskPct > 20
                          ? "text-red-400"
                          : traj.complicationRiskPct > 10
                          ? "text-amber-400"
                          : "text-emerald-400"
                      }
                    >
                      {traj.complicationRiskPct}%
                    </strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Cost:</span>
                    <strong className="text-slate-200">
                      {traj.totalMedicalCost === 0 ? "Free" : `$${traj.totalMedicalCost.toLocaleString()}`}
                    </strong>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
