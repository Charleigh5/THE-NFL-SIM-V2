import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Dna, Gauge, Zap, ShieldAlert, Eye, Lock, Activity, Ruler } from "lucide-react";
import type { BioMetrics } from "../../types/medical";

interface GenesisBiometricCardProps {
  biometrics?: BioMetrics | null;
  playerName?: string;
  position?: string;
  isScoutedInitially?: boolean;
}

export const GenesisBiometricCard: React.FC<GenesisBiometricCardProps> = ({
  biometrics,
  playerName = "Player",
  position = "ATH",
  isScoutedInitially = false,
}) => {
  const [isRevealed, setIsRevealed] = useState(
    isScoutedInitially || biometrics?.genesis_revealed || false
  );

  // Defaults derived or mocked if backend biometrics are loading
  const s2Score = biometrics?.s2_cognition_score ?? 84;
  const gpsSpeed = biometrics?.gps_speed_max ?? 21.4;
  const powerClean = biometrics?.power_clean_max ?? 335;
  const fastTwitch = biometrics ? Math.round(biometrics.fast_twitch_ratio * 100) : 76;
  const wingspan = biometrics?.wingspan_inches ?? 78.5;
  const handSize = biometrics?.hand_size_inches ?? 9.75;
  const medicalFlags = biometrics?.medical_flags ?? ["Prior ACL Reconstruction (College, 2022)"];

  return (
    <div className="relative w-full rounded-2xl bg-gradient-to-br from-slate-900/90 via-slate-950 to-indigo-950/40 border border-slate-800/80 p-5 shadow-2xl backdrop-blur-xl overflow-hidden font-sans">
      {/* Background Accent Gradients */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 mb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Dna className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white tracking-wide uppercase flex items-center gap-2">
              GENESIS Biometric Dossier
              <span className="px-1.5 py-0.2 text-[10px] font-mono rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                PROPRIETARY
              </span>
            </h3>
            <p className="text-[11px] text-slate-400 font-mono">
              {playerName} • {position} Physiology Profile
            </p>
          </div>
        </div>

        {!isRevealed && (
          <button
            onClick={() => setIsRevealed(true)}
            className="flex items-center gap-1.5 px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-semibold tracking-wider transition-all shadow-lg shadow-cyan-950"
          >
            <Eye className="w-3.5 h-3.5" /> Reveal Full Bio-Scan
          </button>
        )}
      </div>

      {/* Content Area with Blur Lock for Unrevealed Mode */}
      <div className="relative">
        <AnimatePresence>
          {!isRevealed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-slate-950/80 backdrop-blur-md rounded-xl p-6 text-center border border-slate-800"
            >
              <div className="p-3 bg-slate-900 rounded-full border border-slate-700 text-cyan-400 mb-2">
                <Lock className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-white mb-1">
                Classified GENESIS Scouting Data
              </h4>
              <p className="text-xs text-slate-400 max-w-sm mb-4">
                Advanced S2 Cognition, GPS tracking telemetry, and medical risk flags require
                authorization to inspect.
              </p>
              <button
                onClick={() => setIsRevealed(true)}
                className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-lg"
              >
                Authorize Decryption
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Primary Metrics Grid */}
        <div
          className={`grid grid-cols-1 md:grid-cols-3 gap-3 ${!isRevealed ? "filter blur-sm select-none pointer-events-none" : ""}`}
        >
          {/* 1. S2 Cognition Dial */}
          <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-xl flex flex-col justify-between">
            <div className="flex justify-between items-start mb-2">
              <span className="text-[11px] font-mono text-slate-400 uppercase flex items-center gap-1.5">
                <Gauge className="w-3.5 h-3.5 text-cyan-400" /> S2 Cognition
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-cyan-950/80 text-cyan-300 border border-cyan-700/40">
                {s2Score >= 80 ? "ELITE READ" : "STANDARD"}
              </span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-black text-white font-mono">{s2Score}</span>
              <span className="text-xs text-slate-400">th Percentile</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-2">
              <div
                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full"
                style={{ width: `${s2Score}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              OODA Loop Reaction: {Math.round(380 - s2Score * 1.5)}ms (Decide & Act speed)
            </p>
          </div>

          {/* 2. GPS Speed Max */}
          <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-xl flex flex-col justify-between">
            <div className="flex justify-between items-start mb-2">
              <span className="text-[11px] font-mono text-slate-400 uppercase flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-amber-400" /> Max In-Game GPS
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-950/80 text-amber-300 border border-amber-700/40">
                TOP BURST
              </span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-black text-white font-mono">
                {gpsSpeed.toFixed(1)}
              </span>
              <span className="text-xs text-slate-400">MPH</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-2">
              <div
                className="bg-gradient-to-r from-amber-500 to-orange-500 h-full rounded-full"
                style={{ width: `${Math.min(100, (gpsSpeed / 24) * 100)}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              Fast-Twitch Ratio: {fastTwitch}% • Explosive Burst Ready
            </p>
          </div>

          {/* 3. Power Clean Max */}
          <div className="bg-slate-900/80 border border-slate-800 p-3.5 rounded-xl flex flex-col justify-between">
            <div className="flex justify-between items-start mb-2">
              <span className="text-[11px] font-mono text-slate-400 uppercase flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5 text-emerald-400" /> Power Clean Max
              </span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-700/40">
                FORCE LOAD
              </span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-black text-white font-mono">{powerClean}</span>
              <span className="text-xs text-slate-400">LBS</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-2">
              <div
                className="bg-gradient-to-r from-emerald-500 to-teal-500 h-full rounded-full"
                style={{ width: `${Math.min(100, (powerClean / 420) * 100)}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              Lower Kinetic Chain Force Output Rating: High
            </p>
          </div>
        </div>

        {/* Secondary Proportions & Flags Row */}
        <div
          className={`grid grid-cols-1 md:grid-cols-2 gap-3 mt-3 ${!isRevealed ? "filter blur-sm select-none pointer-events-none" : ""}`}
        >
          {/* Anatomical Dimensions */}
          <div className="bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-slate-800 text-slate-300">
                <Ruler className="w-4 h-4" />
              </div>
              <div>
                <div className="text-xs font-semibold text-white">Anatomical Levers</div>
                <div className="text-[11px] text-slate-400">
                  Wingspan:{" "}
                  <span className="font-mono text-cyan-300 font-bold">{wingspan.toFixed(1)}"</span>{" "}
                  | Hand Size:{" "}
                  <span className="font-mono text-cyan-300 font-bold">{handSize.toFixed(2)}"</span>
                </div>
              </div>
            </div>
            <div className="text-right text-[10px] font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/30 px-2 py-0.5 rounded">
              +4.2% Reach Advantage
            </div>
          </div>

          {/* Medical Flags */}
          <div className="bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-amber-950/80 text-amber-400 border border-amber-800/40">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div>
                <div className="text-xs font-semibold text-white">Medical History Flags</div>
                <div className="text-[11px] text-amber-300/90 font-mono">
                  {medicalFlags.length > 0 ? medicalFlags.join(", ") : "No chronic pathology flags"}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
