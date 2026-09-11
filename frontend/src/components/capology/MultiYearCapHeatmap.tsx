import React from "react";
import { TrendingUp, Skull } from "lucide-react";
import type { YearlyCapLiability } from "../../types/capology";

interface MultiYearCapHeatmapProps {
  schedule: YearlyCapLiability[];
  loading?: boolean;
}

export const MultiYearCapHeatmap: React.FC<MultiYearCapHeatmapProps> = ({
  schedule,
  loading = false,
}) => {
  if (!schedule || schedule.length === 0) {
    return (
      <div className="h-48 flex items-center justify-center bg-slate-900/60 border border-slate-800 rounded-xl text-slate-500 text-xs">
        No projection schedule available.
      </div>
    );
  }

  // Maximum cap across the 5 years to scale bar heights
  const maxCap = Math.max(...schedule.map((s) => s.projected_cap), 320_000_000);

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-4 text-slate-100">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-200">
            5-Year Franchise Capology Heatmap
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
          <span className="inline-block w-2 h-2 rounded-full bg-emerald-400" />
          <span>Compliant</span>
          <span className="inline-block w-2 h-2 rounded-full bg-rose-500 ml-2" />
          <span>Deficit</span>
        </div>
      </div>

      {/* 5-Column Bar Grid */}
      <div className={`grid grid-cols-5 gap-2.5 pt-2 ${loading ? "opacity-60 transition-opacity" : ""}`}>
        {schedule.map((item) => {
          const projectedMillions = (item.projected_cap / 1_000_000).toFixed(1);
          const committedPct = Math.min(100, (item.committed_salaries / maxCap) * 100);
          const proposedPct = Math.min(100, (item.proposed_contract_cap_hit / maxCap) * 100);
          const deadPct = Math.min(100, (item.dead_money / maxCap) * 100);
          const netMillions = (item.net_cap_space / 1_000_000).toFixed(1);
          const isNegative = item.net_cap_space < 0;

          return (
            <div
              key={item.year}
              className="flex flex-col items-center bg-slate-950/60 rounded-lg p-2 border border-slate-800/80 hover:border-slate-700 transition-colors"
            >
              {/* Year & Projected Cap */}
              <div className="text-center mb-2">
                <span className="text-xs font-bold text-slate-200 block">{item.year}</span>
                <span className="text-[10px] text-slate-400 font-mono">${projectedMillions}M Cap</span>
              </div>

              {/* Stacked Vertical Bar */}
              <div className="w-full h-36 bg-slate-900 rounded-md relative flex flex-col-reverse p-1 overflow-hidden border border-slate-800">
                {/* 1. Committed Salaries (Navy) */}
                {item.committed_salaries > 0 && (
                  <div
                    style={{ height: `${committedPct}%` }}
                    className="w-full bg-slate-700 rounded-sm hover:brightness-125 transition-all"
                    title={`Committed: $${(item.committed_salaries / 1_000_000).toFixed(1)}M`}
                  />
                )}

                {/* 2. Proposed Contract Cap Hit (Gold) */}
                {item.proposed_contract_cap_hit > 0 && (
                  <div
                    style={{ height: `${proposedPct}%` }}
                    className="w-full bg-amber-500 rounded-sm hover:brightness-125 transition-all mt-0.5 shadow-sm shadow-amber-500/50"
                    title={`Proposed Cap Hit: $${(item.proposed_contract_cap_hit / 1_000_000).toFixed(1)}M`}
                  />
                )}

                {/* 3. Accelerated Dead Money (Crimson) */}
                {item.dead_money > 0 && (
                  <div
                    style={{ height: `${deadPct}%` }}
                    className="w-full bg-rose-500 rounded-sm hover:brightness-125 transition-all mt-0.5 relative flex items-center justify-center animate-pulse"
                    title={`Dead Money: $${(item.dead_money / 1_000_000).toFixed(1)}M`}
                  >
                    <Skull className="w-3 h-3 text-white/90" />
                  </div>
                )}
              </div>

              {/* Net Space Metric */}
              <div className="mt-2 text-center w-full">
                <div
                  className={`text-[11px] font-bold font-mono px-1.5 py-0.5 rounded ${
                    isNegative
                      ? "bg-rose-950/80 text-rose-400 border border-rose-800"
                      : "bg-emerald-950/80 text-emerald-400 border border-emerald-800"
                  }`}
                >
                  {isNegative ? `-$${Math.abs(Number(netMillions))}M` : `+$${netMillions}M`}
                </div>
                <span className="text-[9px] text-slate-500 block mt-0.5">
                  {isNegative ? "Deficit" : "Room"}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend & Summary */}
      <div className="flex flex-wrap items-center justify-between pt-2 border-t border-slate-800 text-[11px] text-slate-400 gap-2">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-sm bg-slate-700" />
            <span>Committed</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-sm bg-amber-500" />
            <span>Proposed Offer</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-sm bg-rose-500" />
            <span>Accelerated Dead Money</span>
          </div>
        </div>
        <div className="text-[10px] text-slate-500">
          Source: NFL CBA 5.5% annual cap inflator
        </div>
      </div>
    </div>
  );
};
