import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Activity,
  BedDouble,
  Scissors,
  Sparkles,
  AlertTriangle,
  X,
  Syringe,
  ShieldAlert,
  Clock,
  HeartPulse,
} from 'lucide-react';
import type { MedicalProtocolType, OrthopedicProtocolOption } from '../../types/deepDive';

interface OrthopedicTriageModalProps {
  isOpen: boolean;
  playerId?: number;
  playerName?: string;
  zoneKey: string;
  zoneName: string;
  currentIntegrity: number;
  baselineWeeks?: number;
  onClose: () => void;
  onConfirmProtocol: (protocol: MedicalProtocolType) => void;
}

export const OrthopedicTriageModal: React.FC<OrthopedicTriageModalProps> = ({
  isOpen,
  playerId = 1,
  playerName = 'Selected Athlete',
  zoneKey = 'zone',
  zoneName,
  currentIntegrity,
  baselineWeeks = 4,
  onClose,
  onConfirmProtocol,
}) => {
  const [selectedProtocol, setSelectedProtocol] = useState<MedicalProtocolType>('REST');

  const protocols = React.useMemo<OrthopedicProtocolOption[]>(() => {
    return [
      {
        protocol: 'REST',
        name: 'Conservative Rest & Physical Therapy',
        estimated_recovery_weeks: Math.max(1, baselineWeeks),
        complication_risk_pct: 0.0,
        target_integrity_restore: 100.0,
        re_injury_hazard_multiplier: 1.0,
        game_availability_status: 'OUT',
        description: `Non-invasive physiological rest for ${zoneName.toLowerCase()}. Eliminates complication risks; safe return timetable.`,
        clinical_note: 'Recommended baseline for low-grade muscular strains.',
      },
      {
        protocol: 'PRP_THERAPY',
        name: 'Platelet-Rich Plasma (PRP) Biotherapy',
        estimated_recovery_weeks: Math.max(1, Math.round(baselineWeeks * 0.7)),
        complication_risk_pct: 0.05,
        target_integrity_restore: 95.0,
        re_injury_hazard_multiplier: 1.1,
        game_availability_status: 'OUT',
        description: 'Concentrated autologous platelet injections accelerating cellular regeneration by ~30%.',
        clinical_note: 'Accelerates ligament repair with minimal tissue disturbance.',
      },
      {
        protocol: 'ARTHROSCOPIC_SURGERY',
        name: 'Accelerated Arthroscopic Scope',
        estimated_recovery_weeks: Math.max(1, Math.round(baselineWeeks * 0.5)),
        complication_risk_pct: 0.12,
        target_integrity_restore: 90.0,
        re_injury_hazard_multiplier: 1.25,
        game_availability_status: 'OUT',
        description: 'Surgical scope debridement repairing structural tissue, cutting timetable in half.',
        clinical_note: 'Meniscus and labral cleanouts with faster return to field.',
      },
      {
        protocol: 'RECONSTRUCTIVE_SURGERY',
        name: 'Full Structural Reconstruction',
        estimated_recovery_weeks: Math.max(4, Math.round(baselineWeeks * 1.2)),
        complication_risk_pct: 0.08,
        target_integrity_restore: 98.0,
        re_injury_hazard_multiplier: 0.9,
        game_availability_status: 'OUT',
        description: 'Definitive tendon/ligament graft reconstruction ensuring maximum multi-year joint longevity.',
        clinical_note: 'Best long-term outcome for high-impact contact positions.',
      },
      {
        protocol: 'CORTISONE_STABILIZATION',
        name: 'Cortisone Joint Injection (Suit Up & Play)',
        estimated_recovery_weeks: 0,
        complication_risk_pct: 0.35,
        target_integrity_restore: Math.max(35.0, currentIntegrity),
        re_injury_hazard_multiplier: 2.5,
        game_availability_status: 'QUESTIONABLE',
        description: 'High-dose anti-inflammatory injection with joint bracing allowing the player to suit up immediately.',
        clinical_note: 'WARNING: 2.5x higher hazard of season-ending catastrophic aggravation.',
      },
    ];
  }, [baselineWeeks, zoneName, currentIntegrity]);

  if (!isOpen) return null;

  const protocolIcons: Record<MedicalProtocolType, React.FC<{ className?: string }>> = {
    REST: BedDouble,
    PRP_THERAPY: Syringe,
    ARTHROSCOPIC_SURGERY: Scissors,
    RECONSTRUCTIVE_SURGERY: HeartPulse,
    CORTISONE_STABILIZATION: ShieldAlert,
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-lg p-4 font-sans">
      <motion.div
        initial={{ scale: 0.94, opacity: 0, y: 15 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.94, opacity: 0, y: 15 }}
        className="bg-slate-900/95 border border-cyan-500/30 p-6 rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden"
      >
        {/* Modal Header */}
        <div className="flex justify-between items-start pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-cyan-950/80 border border-cyan-500/40 text-cyan-400">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px] font-mono uppercase font-bold">
                  Orthopedic Triage Hub
                </span>
                <h3 className="text-lg font-bold text-white tracking-wide">{zoneName} Triage</h3>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Patient: <strong className="text-slate-200">{playerName}</strong> (ID #{playerId}) • Zone: <span className="font-mono text-slate-300">{zoneKey}</span> • Current Integrity:{' '}
                <span className="font-mono text-cyan-400 font-bold">{Math.round(currentIntegrity)}%</span>
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

        {/* 5 Clinical Protocols */}
        <div className="mt-4 space-y-3 max-h-[420px] overflow-y-auto pr-1">
          {protocols.map((option) => {
            const Icon = protocolIcons[option.protocol];
            const isSelected = selectedProtocol === option.protocol;

            return (
              <div
                key={option.protocol}
                onClick={() => setSelectedProtocol(option.protocol)}
                className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-start gap-4 ${
                  isSelected
                    ? 'bg-cyan-950/60 border-cyan-400 shadow-[0_0_15px_rgba(0,240,255,0.2)]'
                    : 'bg-slate-950/50 border-slate-800 hover:bg-slate-900/60 hover:border-slate-700'
                }`}
              >
                <div
                  className={`p-3 rounded-xl border ${
                    isSelected
                      ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50'
                      : 'bg-slate-900 text-slate-400 border-slate-800'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                </div>

                <div className="flex-1">
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                    <span className="font-bold text-sm text-slate-100">{option.name}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">
                        {option.estimated_recovery_weeks === 0
                          ? '0 Wks (Suit Up)'
                          : `~${option.estimated_recovery_weeks} Wks`}
                      </span>
                      <span
                        className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold ${
                          option.game_availability_status === 'QUESTIONABLE'
                            ? 'bg-amber-950 text-amber-300 border border-amber-800'
                            : 'bg-red-950 text-red-300 border border-red-800'
                        }`}
                      >
                        {option.game_availability_status}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-400 leading-relaxed mb-2">{option.description}</p>

                  <div className="flex flex-wrap items-center gap-4 text-[10px] font-mono text-slate-400 pt-2 border-t border-slate-800/60">
                    <span className="flex items-center gap-1">
                      <AlertTriangle className="w-3 h-3 text-amber-400" />
                      Complication Risk:{' '}
                      <strong className="text-amber-300 font-bold">
                        {Math.round(option.complication_risk_pct * 100)}%
                      </strong>
                    </span>
                    <span className="flex items-center gap-1">
                      <Sparkles className="w-3 h-3 text-emerald-400" />
                      Target Restore:{' '}
                      <strong className="text-emerald-300 font-bold">
                        {option.target_integrity_restore}%
                      </strong>
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-cyan-400" />
                      Hazard Multiplier:{' '}
                      <strong className="text-cyan-300 font-bold">
                        {option.re_injury_hazard_multiplier}x
                      </strong>
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer Actions */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono font-bold rounded-xl transition-colors uppercase tracking-wider"
          >
            Cancel
          </button>

          <button
            onClick={() => onConfirmProtocol(selectedProtocol)}
            className="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-black text-xs font-mono font-bold rounded-xl shadow-lg shadow-cyan-500/20 transition-all uppercase tracking-wider active:scale-95"
          >
            Apply Protocol & Begin Recovery
          </button>
        </div>
      </motion.div>
    </div>
  );
};
