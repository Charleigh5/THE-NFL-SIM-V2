import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BedDouble, Scissors, ShieldAlert, Sparkles, AlertTriangle, X } from "lucide-react";
import type { TreatmentType, SurgeryRisk } from "../../types/medical";
import { medicalApi } from "../../services/medicalApi";

interface TreatmentModalProps {
  isOpen: boolean;
  playerId?: number;
  playerName?: string;
  partName: string;
  currentHealth: number;
  injurySeverity?: number;
  weeksRemaining?: number;
  onClose: () => void;
  onConfirm: (treatment: TreatmentType) => void;
}

export const TreatmentModal: React.FC<TreatmentModalProps> = ({
  isOpen,
  playerId,
  playerName = "Selected Player",
  partName,
  currentHealth,
  injurySeverity = 4,
  weeksRemaining = 4,
  onClose,
  onConfirm,
}) => {
  const [surgeryRisk, setSurgeryRisk] = useState<SurgeryRisk | null>(null);
  const [loadingRisk, setLoadingRisk] = useState(false);

  useEffect(() => {
    let isCancelled = false;
    if (isOpen && playerId) {
      medicalApi
        .getSurgeryRisk(playerId)
        .then((data) => {
          if (!isCancelled) {
            setSurgeryRisk(data);
            setLoadingRisk(false);
          }
        })
        .catch(() => {
          if (!isCancelled) {
            // Default mathematical calculation from backend if endpoint is unavailable
            const baseRisk = 0.05;
            const severityRisk = (injurySeverity || 4) * 0.01;
            const totalRisk = Math.min(0.25, baseRisk + severityRisk);
            setSurgeryRisk({
              player_id: playerId,
              base_risk: baseRisk,
              age_risk: 0.01,
              severity_risk: severityRisk,
              total_risk: totalRisk,
              estimated_recovery_reduction: 0.4,
            });
            setLoadingRisk(false);
          }
        });
    }
    return () => {
      isCancelled = true;
    };
  }, [isOpen, playerId, injurySeverity]);

  if (!isOpen) return null;

  const estimatedSurgeryWeeks = Math.max(
    1,
    Math.round(weeksRemaining * (1 - (surgeryRisk?.estimated_recovery_reduction ?? 0.4)))
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4">
      <motion.div
        className="bg-slate-900 border border-cyan-500/30 p-6 rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden font-sans"
        initial={{ scale: 0.92, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.92, opacity: 0, y: 20 }}
      >
        {/* Header */}
        <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px] font-mono uppercase font-bold">
                Medical Decision Hub
              </span>
              <h2 className="text-xl font-bold text-white tracking-wide">
                {partName} Diagnosis & Treatment
              </h2>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Patient: <strong className="text-slate-200">{playerName}</strong> • Zone Integrity:{" "}
              <span className="font-mono text-cyan-400 font-bold">
                {Math.round(currentHealth)}%
              </span>{" "}
              • Est. Recovery:{" "}
              <span className="font-mono text-amber-400 font-bold">{weeksRemaining} Weeks</span>
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Treatment Options */}
        <div className="space-y-3.5">
          {/* 1. REST */}
          <div
            onClick={() => onConfirm("REST")}
            className="group flex items-start gap-4 p-4 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800/80 hover:border-emerald-500/50 cursor-pointer transition-all"
          >
            <div className="p-3 rounded-xl bg-emerald-950/80 text-emerald-400 border border-emerald-800/40 group-hover:scale-105 transition-transform">
              <BedDouble className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-center mb-1">
                <span className="font-bold text-base text-slate-100 group-hover:text-emerald-300 transition-colors">
                  Standard Rest & Rehabilitation
                </span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  {weeksRemaining} Weeks
                </span>
              </div>
              <p className="text-xs text-slate-400 mb-2 leading-relaxed">
                Conservative non-invasive recovery protocol. Eliminates aggravation risk; player
                remains inactive (OUT).
              </p>
              <div className="flex items-center gap-2 text-[10px] font-mono text-emerald-400">
                <Sparkles className="w-3.5 h-3.5" /> 0% Complication Risk • Safe Baseline
              </div>
            </div>
          </div>

          {/* 2. SURGERY */}
          <div
            onClick={() => onConfirm("SURGERY")}
            className="group flex items-start gap-4 p-4 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800/80 hover:border-cyan-500/50 cursor-pointer transition-all"
          >
            <div className="p-3 rounded-xl bg-cyan-950/80 text-cyan-400 border border-cyan-800/40 group-hover:scale-105 transition-transform">
              <Scissors className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-center mb-1">
                <span className="font-bold text-base text-slate-100 group-hover:text-cyan-300 transition-colors">
                  Accelerated Surgical Repair
                </span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                  ~{estimatedSurgeryWeeks} Weeks (-40%)
                </span>
              </div>
              <p className="text-xs text-slate-400 mb-2 leading-relaxed">
                Repairs structural tissue. Accelerates timetable by 30-50%, but carries a calculated
                complication risk.
              </p>
              <div className="flex items-center gap-2 text-[10px] font-mono text-cyan-400">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                {loadingRisk ? (
                  "Calculating surgical risk..."
                ) : (
                  <span>
                    Complication Risk:{" "}
                    <strong className="text-amber-300 font-bold">
                      {Math.round((surgeryRisk?.total_risk ?? 0.1) * 100)}%
                    </strong>{" "}
                    (Adds +2-6 wks if failed)
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* 3. PLAY THROUGH */}
          <div
            onClick={() => onConfirm("PLAY_THROUGH")}
            className="group flex items-start gap-4 p-4 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800/80 hover:border-amber-500/50 cursor-pointer transition-all"
          >
            <div className="p-3 rounded-xl bg-amber-950/80 text-amber-400 border border-amber-800/40 group-hover:scale-105 transition-transform">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <div className="flex justify-between items-center mb-1">
                <span className="font-bold text-base text-slate-100 group-hover:text-amber-300 transition-colors">
                  Field Stabilization (Play Through)
                </span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">
                  QUESTIONABLE
                </span>
              </div>
              <p className="text-xs text-slate-400 mb-2 leading-relaxed">
                Applies braces/injections. Player dresses for game day with stat penalties (reduced
                if high Toughness / Ragknow).
              </p>
              <div className="flex items-center gap-2 text-[10px] font-mono text-amber-400">
                <AlertTriangle className="w-3.5 h-3.5" /> High In-Game Escalation Risk • Speed &
                Agility Penalty
              </div>
            </div>
          </div>
        </div>

        <div className="mt-5 pt-3 border-t border-slate-800/80 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-lg transition-colors uppercase tracking-wider"
          >
            Close
          </button>
        </div>
      </motion.div>
    </div>
  );
};
