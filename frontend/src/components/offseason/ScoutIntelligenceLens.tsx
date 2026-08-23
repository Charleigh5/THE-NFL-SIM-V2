import React from "react";
import { motion } from "framer-motion";
import { Brain, Gauge, Sparkles, ShieldAlert, FileText, Zap, Compass } from "lucide-react";
import type { ScoutBiasLens, ProspectIntelligence } from "../../types/deepDive";

interface ScoutIntelligenceLensProps {
  currentLens: ScoutBiasLens;
  onLensChange: (lens: ScoutBiasLens) => void;
  selectedProspect?: ProspectIntelligence | null;
}

const LENS_METADATA: Record<
  ScoutBiasLens,
  { label: string; icon: React.FC<{ className?: string }>; color: string; desc: string }
> = {
  CONSENSUS: {
    label: "Media Consensus",
    icon: Compass,
    color: "#00f0ff",
    desc: "National draft boards and aggregated media ranking composite.",
  },
  FILM_TRADITIONALIST: {
    label: "Film Room Guru",
    icon: FileText,
    color: "#f59e0b",
    desc: "Heavy weight on S2 cognition, pre-snap processing, and technique.",
  },
  ANALYTICS_METRICS: {
    label: "Analytics & GPS",
    icon: Gauge,
    color: "#10b981",
    desc: "Peak GPS tracking speed, burst acceleration index, and age curves.",
  },
  REGIONAL_SCOUT: {
    label: "Area Scout Note",
    icon: Zap,
    color: "#ec4899",
    desc: "Visceral subjective evaluation with high upside conviction bias.",
  },
};

export const ScoutIntelligenceLens: React.FC<ScoutIntelligenceLensProps> = ({
  currentLens,
  onLensChange,
  selectedProspect,
}) => {
  const activeMeta = LENS_METADATA[currentLens];

  return (
    <div className="w-full bg-slate-950/80 border border-slate-800/90 rounded-2xl p-4 shadow-2xl backdrop-blur-xl mb-4 font-sans">
      {/* Header & Lens Buttons */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-cyan-950/80 border border-cyan-500/30 text-cyan-400">
            <Brain className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-mono font-bold tracking-wider text-slate-200 uppercase">
              Scouting Fog-of-War Lens
            </h4>
            <p className="text-[11px] text-slate-400">{activeMeta.desc}</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-1.5 p-1 bg-slate-900/90 border border-slate-800 rounded-xl">
          {(Object.keys(LENS_METADATA) as ScoutBiasLens[]).map((lens) => {
            const meta = LENS_METADATA[lens];
            const Icon = meta.icon;
            const isActive = currentLens === lens;
            return (
              <button
                key={lens}
                onClick={() => onLensChange(lens)}
                className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
                  isActive
                    ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-[0_0_10px_rgba(0,240,255,0.2)]"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{meta.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Dynamic Prospect Lens Inspection (if selected) */}
      {selectedProspect && (
        <motion.div
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-3 grid grid-cols-2 md:grid-cols-5 gap-3 pt-2"
        >
          {/* Perceived OVR */}
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Lens Grade</span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-lg font-extrabold text-cyan-400 font-mono">
                {selectedProspect.perceived_ovr[currentLens] ?? selectedProspect.consensus_ovr}
              </span>
              <span className="text-[10px] text-slate-500 font-mono">OVR</span>
            </div>
          </div>

          {/* S2 Cognition */}
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col">
            <span className="text-[10px] font-mono text-slate-400 uppercase">S2 Cognition</span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-lg font-extrabold text-emerald-400 font-mono">
                {selectedProspect.s2_cognition_score}
              </span>
              <span className="text-[10px] text-emerald-500/70 font-mono">/ 100</span>
            </div>
          </div>

          {/* Peak GPS Speed */}
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col">
            <span className="text-[10px] font-mono text-slate-400 uppercase">GPS Top Speed</span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span className="text-lg font-extrabold text-amber-400 font-mono">
                {selectedProspect.gps_speed_max}
              </span>
              <span className="text-[10px] text-amber-500/70 font-mono">MPH</span>
            </div>
          </div>

          {/* Boom / Bust Factor */}
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Boom / Bust Risk</span>
            <div className="flex items-baseline gap-1 mt-0.5">
              <span
                className={`text-lg font-extrabold font-mono ${
                  selectedProspect.boom_bust_factor > 0.6
                    ? "text-red-400"
                    : selectedProspect.boom_bust_factor > 0.3
                      ? "text-amber-400"
                      : "text-emerald-400"
                }`}
              >
                {Math.round(selectedProspect.boom_bust_factor * 100)}%
              </span>
              <Sparkles className="w-3 h-3 text-slate-500 ml-1" />
            </div>
          </div>

          {/* Medical Grade */}
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Medical Flag</span>
            <div className="flex items-center gap-1.5 mt-1">
              <ShieldAlert
                className={`w-4 h-4 ${
                  selectedProspect.medical_grade === "PASS"
                    ? "text-emerald-400"
                    : selectedProspect.medical_grade === "CONCERN"
                      ? "text-amber-400"
                      : "text-red-400"
                }`}
              />
              <span
                className={`text-xs font-mono font-bold px-1.5 py-0.5 rounded ${
                  selectedProspect.medical_grade === "PASS"
                    ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                    : selectedProspect.medical_grade === "CONCERN"
                      ? "bg-amber-950 text-amber-300 border border-amber-800"
                      : "bg-red-950 text-red-300 border border-red-800"
                }`}
              >
                {selectedProspect.medical_grade}
              </span>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};
