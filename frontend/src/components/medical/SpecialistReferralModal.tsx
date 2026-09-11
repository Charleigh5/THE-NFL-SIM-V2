import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Building2,
  Stethoscope,
  ShieldCheck,
  AlertOctagon,
  Clock,
  DollarSign,
  CheckCircle2,
  X,
  Loader2,
  Sparkles,
} from "lucide-react";
import type {
  SecondOpinionCenter,
  SecondOpinionConsultResult,
} from "../../types/orthopedicRtp";
import { orthopedicApi } from "../../services/orthopedicApi";

interface SpecialistReferralModalProps {
  isOpen: boolean;
  onClose: () => void;
  playerId: number;
  playerName: string;
  injuryType: string;
  onConsultSuccess?: (result: SecondOpinionConsultResult) => void;
}

export const SpecialistReferralModal: React.FC<SpecialistReferralModalProps> = ({
  isOpen,
  onClose,
  playerId,
  playerName,
  injuryType,
  onConsultSuccess,
}) => {
  const [centers, setCenters] = useState<SecondOpinionCenter[]>([]);
  const [selectedCenterId, setSelectedCenterId] = useState<string>("andrews_sports_med");
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [consultResult, setConsultResult] = useState<SecondOpinionConsultResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!isOpen) {
      setConsultResult(null);
      setErrorMessage(null);
      return;
    }

    let isCancelled = false;
    setIsLoading(true);
    orthopedicApi
      .getSpecialistCenters()
      .then((data) => {
        if (!isCancelled) {
          setCenters(data);
          if (data.length > 0) {
            setSelectedCenterId(data[0].centerId);
          }
        }
      })
      .catch((err) => {
        if (!isCancelled) {
          console.warn("Failed to load centers, using defaults:", err);
        }
      })
      .finally(() => {
        if (!isCancelled) setIsLoading(false);
      });

    return () => {
      isCancelled = true;
    };
  }, [isOpen]);

  const handleRequestConsult = async () => {
    if (!selectedCenterId) return;
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const result = await orthopedicApi.consultSpecialist({
        playerId,
        centerId: selectedCenterId,
      });
      setConsultResult(result);
      if (onConsultSuccess) {
        onConsultSuccess(result);
      }
    } catch (err: unknown) {
      console.error("Consultation failed:", err);
      setErrorMessage("Failed to complete outside consultation. Check network connectivity.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4 font-sans">
      <motion.div
        initial={{ scale: 0.94, opacity: 0, y: 15 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.94, opacity: 0, y: 15 }}
        className="bg-slate-900 border border-cyan-500/30 p-6 rounded-3xl w-full max-w-2xl shadow-2xl relative overflow-hidden"
      >
        {/* Header */}
        <div className="flex justify-between items-start pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-cyan-950/80 border border-cyan-500/40 text-cyan-400">
              <Building2 className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px] font-mono uppercase font-bold">
                  Elite Orthopedic Council
                </span>
                <span className="text-[10px] font-mono text-emerald-400 font-bold">
                  2nd Opinion Referral
                </span>
              </div>
              <h3 className="text-lg font-bold text-white tracking-wide mt-0.5">
                Outside Specialist Consultation
              </h3>
              <p className="text-xs text-slate-400">
                Athlete: <strong className="text-slate-200">{playerName}</strong> • Primary Diagnosis:{" "}
                <span className="text-amber-400 font-mono font-bold">{injuryType}</span>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {errorMessage && (
          <div className="mt-3 p-3 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-xs font-mono">
            {errorMessage}
          </div>
        )}

        {/* Content Body: Centers or Result */}
        <div className="mt-4 max-h-[440px] overflow-y-auto pr-1 space-y-3">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12 text-slate-400 gap-2">
              <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
              <span className="text-xs font-mono">Connecting to National Orthopedic Network...</span>
            </div>
          ) : consultResult ? (
            /* Result View */
            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              className="space-y-4"
            >
              <div
                className={`p-4 rounded-2xl border ${
                  consultResult.occultPathologyDetected
                    ? "bg-amber-950/40 border-amber-500/60"
                    : "bg-emerald-950/40 border-emerald-500/60"
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    {consultResult.occultPathologyDetected ? (
                      <AlertOctagon className="w-5 h-5 text-amber-400" />
                    ) : (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    )}
                    <h4 className="text-sm font-bold text-white font-mono">
                      {consultResult.occultPathologyDetected
                        ? "OCCULT PATHOLOGY DETECTED"
                        : "PRIMARY DIAGNOSIS CONFIRMED"}
                    </h4>
                  </div>
                  <span className="px-2.5 py-0.5 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-300 text-[10px] font-mono font-bold">
                    {consultResult.centerName}
                  </span>
                </div>

                <div className="text-xs font-mono text-slate-300 mb-2">
                  Chief Attending: <strong className="text-white">{consultResult.chiefSurgeon}</strong>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed bg-black/40 p-3 rounded-xl border border-slate-800">
                  {consultResult.findingsNarrative}
                </p>

                <div className="mt-3 flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-800">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-mono text-slate-400">Confirmed:</span>
                    <span className="text-xs font-bold text-slate-100">
                      {consultResult.confirmedDiagnosis}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 text-xs font-mono font-bold">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    <span>50% Surgical Complication Risk Reduction Granted</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ) : (
            /* Clinic Selector */
            <div className="space-y-3">
              <div className="text-xs text-slate-400 leading-relaxed">
                Refer athlete to an independent institute for ultra-high-resolution 3T MRI review and
                surgical consultation. Uncovers occult tears (15% probability) and reduces downstream
                surgical complication risks by <strong>50%</strong>.
              </div>

              {centers.map((center) => {
                const isSelected = selectedCenterId === center.centerId;
                return (
                  <div
                    key={center.centerId}
                    onClick={() => setSelectedCenterId(center.centerId)}
                    className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-start justify-between gap-4 ${
                      isSelected
                        ? "bg-cyan-950/60 border-cyan-400 shadow-[0_0_15px_rgba(0,240,255,0.2)]"
                        : "bg-slate-950/50 border-slate-800 hover:bg-slate-900/60 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className={`p-2.5 rounded-xl border mt-0.5 ${
                          isSelected
                            ? "bg-cyan-500/20 text-cyan-300 border-cyan-500/50"
                            : "bg-slate-900 text-slate-400 border-slate-800"
                        }`}
                      >
                        <Stethoscope className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-bold text-white">{center.name}</h4>
                          {isSelected && (
                            <span className="px-1.5 py-0.2 rounded bg-cyan-900 text-cyan-300 text-[10px] font-mono">
                              Selected
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-cyan-400 font-mono mt-0.5">
                          {center.chiefSurgeon}
                        </p>
                        <p className="text-xs text-slate-400 mt-1">{center.specialtyRegion}</p>

                        <div className="flex items-center gap-4 text-[10px] font-mono text-slate-400 mt-2">
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3 text-cyan-400" />
                            Turnaround: {center.turnaroundDays} Days
                          </span>
                          <span className="flex items-center gap-1">
                            <Sparkles className="w-3 h-3 text-emerald-400" />
                            Diagnostic Boost: +{Math.round(center.diagnosticAccuracyBoost * 100)}%
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="text-right whitespace-nowrap">
                      <div className="text-[10px] text-slate-500 font-mono uppercase">Consult Fee</div>
                      <div className="text-sm font-bold font-mono text-emerald-400 flex items-center justify-end">
                        <DollarSign className="w-3.5 h-3.5" />
                        {center.consultationCost.toLocaleString()}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="mt-5 pt-4 border-t border-slate-800 flex items-center justify-between">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono font-bold rounded-xl transition-colors uppercase tracking-wider"
          >
            {consultResult ? "Close Report" : "Cancel"}
          </button>

          {!consultResult && (
            <button
              onClick={handleRequestConsult}
              disabled={isSubmitting || isLoading || !selectedCenterId}
              className="flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black text-xs font-mono font-bold rounded-xl shadow-lg shadow-cyan-500/20 transition-all uppercase tracking-wider active:scale-95 disabled:opacity-50"
            >
              {isSubmitting && <Loader2 className="w-4 h-4 animate-spin" />}
              {isSubmitting ? "Consulting..." : "Dispatch Athlete for 2nd Opinion"}
            </button>
          )}
        </div>
      </motion.div>
    </div>
  );
};
