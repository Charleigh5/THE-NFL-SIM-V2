import React, { useState } from "react";
import { AlertTriangle, Flame, ShieldAlert, DollarSign, CheckCircle2, UserX } from "lucide-react";
import type { GraphNode, HoldoutAction } from "../../types/socialGraph";

interface HoldoutWarningBannerProps {
  holdoutNodes: GraphNode[];
  onResolveHoldout: (playerId: number, action: HoldoutAction) => Promise<void>;
  onSeedHoldout?: () => Promise<void>;
  isResolving?: boolean;
}

export const HoldoutWarningBanner: React.FC<HoldoutWarningBannerProps> = ({
  holdoutNodes,
  onResolveHoldout,
  onSeedHoldout,
  isResolving = false,
}) => {
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(
    holdoutNodes.length > 0 ? holdoutNodes[0].id : null
  );

  const activeHoldout = holdoutNodes.find((n) => n.id === selectedPlayerId) || holdoutNodes[0];

  if (holdoutNodes.length === 0) {
    return (
      <div className="bg-gradient-to-r from-slate-900/90 via-slate-800/80 to-slate-900/90 border border-emerald-500/30 rounded-2xl p-4 shadow-xl backdrop-blur-md flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center shrink-0">
            <CheckCircle2 size={20} className="text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">
                Locker Room Harmony • Zero Active Holdouts
              </h4>
            </div>
            <p className="text-gray-300 text-xs mt-0.5">
              All 53 rostered athletes are currently active and compliant with franchise contract
              commitments.
            </p>
          </div>
        </div>

        {onSeedHoldout && (
          <button
            onClick={() => onSeedHoldout()}
            disabled={isResolving}
            className="px-3 py-1.5 bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-300 hover:text-white rounded-lg text-xs font-mono uppercase tracking-wider transition-all flex items-center gap-1.5 shrink-0"
          >
            <Flame size={13} className="text-red-400 animate-pulse" />
            <span>Simulate Contract Holdout</span>
          </button>
        )}
      </div>
    );
  }

  return (
    <div
      className="bg-gradient-to-r from-red-950/80 via-rose-950/70 to-red-950/80 border-2 border-red-500/70 rounded-2xl p-5 shadow-2xl backdrop-blur-md relative overflow-hidden"
      data-testid="holdout-warning-banner"
    >
      {/* Background Warning Glow */}
      <div className="absolute -top-12 -right-12 w-48 h-48 bg-red-600/15 rounded-full blur-3xl pointer-events-none" />

      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 relative z-10">
        {/* Left Info Column */}
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-red-600/30 border-2 border-red-500 flex items-center justify-center shrink-0 shadow-lg animate-pulse">
            <Flame size={26} className="text-red-400" />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping" />
              <span className="text-xs font-mono font-bold uppercase tracking-widest text-red-400 flex items-center gap-1">
                <ShieldAlert size={14} />
                CRITICAL HOLDOUT ALERT • {holdoutNodes.length} ATHLETE
                {holdoutNodes.length > 1 ? "S" : ""} BOYCOTTING
              </span>
            </div>

            <div className="mt-1 flex items-center gap-3">
              <h3 className="text-xl font-header font-bold uppercase text-white tracking-wide">
                {activeHoldout.name} ({activeHoldout.position} • {activeHoldout.overall_rating} OVR)
              </h3>
              <span className="px-2 py-0.5 rounded bg-red-500/30 border border-red-500/50 text-[11px] font-mono text-red-300">
                Tension: {activeHoldout.tension_score.toFixed(1)} / 100
              </span>
            </div>

            <p className="text-gray-300 text-xs mt-1 max-w-2xl font-body">
              {activeHoldout.name} has formally ceased team walkthroughs and practice participation
              citing contract undervaluation. Game-day availability is frozen until resolved by
              front office leadership.
            </p>

            {/* Holdout Player Selector (if multiple) */}
            {holdoutNodes.length > 1 && (
              <div className="flex items-center gap-2 mt-2">
                <span className="text-[11px] font-mono text-gray-400">Select athlete:</span>
                <div className="flex gap-1">
                  {holdoutNodes.map((node) => (
                    <button
                      key={node.id}
                      onClick={() => setSelectedPlayerId(node.id)}
                      className={`px-2 py-0.5 rounded text-xs font-mono transition-all ${
                        node.id === activeHoldout.id
                          ? "bg-red-500 text-white font-bold"
                          : "bg-black/40 text-gray-400 hover:text-white border border-white/10"
                      }`}
                    >
                      {node.name}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right GM Actions Column */}
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <button
            onClick={() => onResolveHoldout(activeHoldout.id, "CONCEDE_CONTRACT")}
            disabled={isResolving}
            className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-header text-xs uppercase tracking-wider rounded-xl shadow-lg border border-emerald-400/40 transition-all flex items-center gap-2 active:scale-95 disabled:opacity-50"
            title="Grant contractual sweetener, drops tension by 45, restores active practice status"
          >
            <DollarSign size={15} />
            <span>Concede Contract</span>
          </button>

          <button
            onClick={() => onResolveHoldout(activeHoldout.id, "FINE_DAILY")}
            disabled={isResolving}
            className="px-3.5 py-2.5 bg-amber-600/30 hover:bg-amber-600/50 text-amber-200 hover:text-white font-header text-xs uppercase tracking-wider rounded-xl border border-amber-500/40 transition-all flex items-center gap-2 active:scale-95 disabled:opacity-50"
            title="Levy CBA mandatory $50,000/day unexcused absence fines"
          >
            <AlertTriangle size={15} />
            <span>Fine Daily ($50k)</span>
          </button>

          <button
            onClick={() => onResolveHoldout(activeHoldout.id, "PLACE_ON_RESERVE")}
            disabled={isResolving}
            className="px-3.5 py-2.5 bg-red-900/50 hover:bg-red-900/80 text-rose-300 hover:text-white font-header text-xs uppercase tracking-wider rounded-xl border border-rose-500/40 transition-all flex items-center gap-2 active:scale-95 disabled:opacity-50"
            title="Place on Did Not Report reserve list; withholds weekly game checks"
          >
            <UserX size={15} />
            <span>Deactivate to Reserve</span>
          </button>
        </div>
      </div>
    </div>
  );
};
