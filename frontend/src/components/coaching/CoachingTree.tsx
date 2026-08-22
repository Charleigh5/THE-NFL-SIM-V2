import React, { useState } from "react";
import { motion } from "framer-motion";
import { CoachingDynastyTree } from "./CoachingDynastyTree";
import { Users, GitBranch } from "lucide-react";
import "./CoachingTree.css";

interface CoachNodeProps {
  name: string;
  role: string;
  specialty: string;
  color: string;
}

const CoachNode: React.FC<CoachNodeProps> = ({ name, role, specialty, color }) => (
  <motion.div
    className={`coach-node flex flex-col items-center p-3 rounded-lg border border-opacity-50 min-w-[120px] bg-black/40 backdrop-blur-sm`}
    style={{ "--node-color": color } as React.CSSProperties}
    whileHover={{ scale: 1.05, boxShadow: `0 0 15px ${color}40` }}
  >
    <div className="coach-node-icon w-12 h-12 rounded-full mb-2 flex items-center justify-center font-bold text-white border-2">
      {name.charAt(0)}
    </div>
    <div className="text-xs font-bold text-gray-200">{role}</div>
    <div className="text-sm font-bold text-white mb-1">{name}</div>
    <div className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-white/10 text-gray-400">
      {specialty}
    </div>
  </motion.div>
);

export const CoachingTree: React.FC = () => {
  const [viewMode, setViewMode] = useState<"HIERARCHY" | "SKILL_TREE">("SKILL_TREE");

  return (
    <div className="w-full flex flex-col items-center gap-6 font-sans">
      {/* Mode Switcher */}
      <div className="flex items-center gap-2 p-1.5 bg-slate-900/90 border border-slate-800 rounded-2xl">
        <button
          onClick={() => setViewMode("SKILL_TREE")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono font-bold transition-all ${
            viewMode === "SKILL_TREE"
              ? "bg-cyan-500 text-black shadow-lg shadow-cyan-500/20"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <GitBranch className="w-4 h-4" />
          Dynasty Skill Tree & Synergies
        </button>
        <button
          onClick={() => setViewMode("HIERARCHY")}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono font-bold transition-all ${
            viewMode === "HIERARCHY"
              ? "bg-cyan-500 text-black shadow-lg shadow-cyan-500/20"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <Users className="w-4 h-4" />
          Staff Organizational Chart
        </button>
      </div>

      {viewMode === "SKILL_TREE" ? (
        <CoachingDynastyTree />
      ) : (
        <div className="p-8 flex flex-col items-center relative gap-8 w-full max-w-4xl bg-slate-950/70 border border-slate-800 rounded-3xl backdrop-blur-xl">
          {/* Head Coach */}
          <div className="z-10">
            <CoachNode name="Zac Taylor" role="Head Coach" specialty="Offensive Guru" color="#f59e0b" />
          </div>

          {/* Connection Lines (SVG) */}
          <svg className="absolute top-28 left-0 w-full h-20 -z-0 pointer-events-none">
            <path d="M50% 0 L50% 20 L25% 20 L25% 40" fill="none" stroke="#4b5563" strokeWidth="2" />
            <path d="M50% 20 L75% 20 L75% 40" fill="none" stroke="#4b5563" strokeWidth="2" />
          </svg>

          {/* Coordinators */}
          <div className="flex gap-32 z-10">
            <div className="flex flex-col items-center gap-6">
              <CoachNode
                name="Brian Callahan"
                role="Offensive Coord"
                specialty="Passing Game"
                color="#3b82f6"
              />

              <svg className="w-full h-8 overflow-visible">
                <path
                  d="M50% 0 L50% 32"
                  fill="none"
                  stroke="#4b5563"
                  strokeWidth="1"
                  strokeDasharray="4 2"
                />
              </svg>

              <div className="flex gap-4">
                <CoachNode name="Dan Pitcher" role="QB Coach" specialty="Development" color="#1d4ed8" />
                <CoachNode
                  name="Frank Pollack"
                  role="OL Coach"
                  specialty="Protection"
                  color="#1d4ed8"
                />
              </div>
            </div>

            <div className="flex flex-col items-center gap-6">
              <CoachNode
                name="Lou Anarumo"
                role="Defensive Coord"
                specialty="Schemer"
                color="#ef4444"
              />

              <svg className="w-full h-8 overflow-visible">
                <path
                  d="M50% 0 L50% 32"
                  fill="none"
                  stroke="#4b5563"
                  strokeWidth="1"
                  strokeDasharray="4 2"
                />
              </svg>

              <div className="flex gap-4">
                <CoachNode name="Marion Hobby" role="DL Coach" specialty="Pass Rush" color="#b91c1c" />
                <CoachNode name="Charles Burks" role="DB Coach" specialty="Coverage" color="#b91c1c" />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
