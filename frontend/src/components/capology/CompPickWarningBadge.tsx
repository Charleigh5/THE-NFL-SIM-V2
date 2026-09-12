import React from "react";
import { AlertTriangle, CheckCircle2, Award } from "lucide-react";
import type { CompPickImpact } from "../../types/capology";

interface CompPickWarningBadgeProps {
  impact: CompPickImpact | null;
}

export const CompPickWarningBadge: React.FC<CompPickWarningBadgeProps> = ({ impact }) => {
  if (!impact) return null;

  if (!impact.qualifies_as_cfa) {
    return (
      <div className="flex items-center gap-2 p-2.5 bg-emerald-950/40 border border-emerald-800/40 rounded-lg text-xs text-emerald-300">
        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
        <span>
          <strong>CBA Appendix V:</strong> Under $3.0M APY threshold. No compensatory draft picks
          will be cancelled.
        </span>
      </div>
    );
  }

  return (
    <div className="p-3 bg-amber-950/50 border border-amber-500/40 rounded-xl space-y-2 text-amber-200 shadow-lg shadow-amber-950/30">
      <div className="flex items-start gap-2.5">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-amber-300">
              Compensatory Draft Pick Warning
            </span>
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
              <Award className="w-3 h-3" />
              Tier {impact.cfa_tier} CFA
            </span>
          </div>
          <p className="text-xs text-amber-200/90 leading-relaxed">{impact.impact_summary}</p>
        </div>
      </div>

      {impact.projected_comp_picks_lost.length > 0 && (
        <div className="pt-2 border-t border-amber-800/40 flex flex-wrap gap-1.5">
          {impact.projected_comp_picks_lost.map((pick, idx) => (
            <span
              key={idx}
              className="text-[10px] font-medium bg-rose-900/40 text-rose-300 border border-rose-700/50 px-2 py-0.5 rounded-md"
            >
              Forfeits: {pick}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};
