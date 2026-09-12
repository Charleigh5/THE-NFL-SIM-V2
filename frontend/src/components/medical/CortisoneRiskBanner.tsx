import React from "react";
import { ShieldAlert, AlertTriangle, Activity } from "lucide-react";
import { motion } from "framer-motion";

interface CortisoneRiskBannerProps {
  playerName?: string;
  hazardMultiplier?: number;
  snapsPlayed?: number;
  compact?: boolean;
}

export const CortisoneRiskBanner: React.FC<CortisoneRiskBannerProps> = ({
  playerName = "Athlete",
  hazardMultiplier = 2.5,
  snapsPlayed = 0,
  compact = false,
}) => {
  const isHighSnapRisk = snapsPlayed > 25;

  if (compact) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-red-950/70 border border-red-500/60 shadow-[0_0_12px_rgba(239,68,68,0.3)]">
        <ShieldAlert className="w-4 h-4 text-red-400 animate-pulse" />
        <span className="text-[11px] font-mono font-bold text-red-300 uppercase tracking-wider">
          Cortisone Active: {hazardMultiplier}x Re-Rupture Risk
        </span>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-4 rounded-2xl bg-gradient-to-r from-red-950/80 via-slate-900 to-amber-950/70 border border-red-500/50 shadow-[0_0_20px_rgba(239,68,68,0.25)] relative overflow-hidden"
    >
      {/* Background hazard diagonal stripes */}
      <div className="absolute inset-0 opacity-5 pointer-events-none bg-[repeating-linear-gradient(45deg,#ef4444,#ef4444_10px,transparent_10px,transparent_20px)]" />

      <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-red-500/20 border border-red-500/60 text-red-400">
            <ShieldAlert className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-red-950 border border-red-700 text-red-300 text-[10px] font-mono uppercase font-bold tracking-wider animate-pulse">
                Critical Hazard Warning
              </span>
              <span className="text-xs font-mono text-slate-400">
                Patient: <strong className="text-slate-200">{playerName}</strong>
              </span>
            </div>
            <h4 className="text-sm font-bold text-white tracking-wide mt-0.5 flex items-center gap-2">
              Cortisone Masking Active •{" "}
              <span className="text-red-400 font-mono">
                {hazardMultiplier}x Acute Re-Rupture Hazard
              </span>
            </h4>
            <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
              Pain receptor transmission masked to <strong>95% game-day effectiveness</strong>.
              Severe tissue vulnerability during high-G athletic cuts (&Delta;v &gt; 4.5 m/s&sup2;)
              and contact impacts (p &gt; 850 kg&middot;m/s).
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto justify-end border-t md:border-t-0 pt-2 md:pt-0 border-red-900/50">
          <div className="text-right">
            <div className="text-[10px] text-slate-400 font-mono uppercase">Snap Load Safety</div>
            <div className="flex items-center gap-1.5 font-mono text-xs font-bold">
              <Activity className="w-3.5 h-3.5 text-cyan-400" />
              <span className={isHighSnapRisk ? "text-red-400" : "text-emerald-400"}>
                {snapsPlayed} / 25 Max
              </span>
            </div>
          </div>
          <div className="p-2 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-xs font-mono font-bold flex items-center gap-1">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
            <span>High Cut Risk</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
