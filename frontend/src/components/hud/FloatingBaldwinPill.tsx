/**
 * Floating Baldwin 4th-Down Decision Pill
 * ========================================
 * Unobtrusive glassmorphic HUD pill docked to the top-right field viewport.
 * Provides instant analytical clarity on 4th down without obstructing on-field player tracking.
 */

import React, { useState } from "react";
import { Sparkles, X, Check } from "lucide-react";
import type { FourthDownTelemetryPayload } from "../../types/hudTelemetry";

interface FloatingBaldwinPillProps {
  telemetry: FourthDownTelemetryPayload | null;
  onConfirmRecommendation?: (action: "GO" | "FIELD_GOAL" | "PUNT") => void;
  onDismiss?: () => void;
  className?: string;
}

export const FloatingBaldwinPill: React.FC<FloatingBaldwinPillProps> = ({
  telemetry,
  onConfirmRecommendation,
  onDismiss,
  className = "",
}) => {
  const [isHovered, setIsHovered] = useState(false);

  if (!telemetry) return null;

  const getActionColor = (action: string) => {
    switch (action) {
      case "GO":
        return {
          pill: "bg-emerald-950/80 border-emerald-500/50 text-emerald-300 shadow-emerald-950/60 shadow-lg",
          badge: "bg-emerald-500 text-black shadow-sm font-extrabold",
          highlight: "text-emerald-400",
          border: "border-emerald-500/30",
        };
      case "FIELD_GOAL":
        return {
          pill: "bg-amber-950/80 border-amber-500/50 text-amber-300 shadow-amber-950/60 shadow-lg",
          badge: "bg-amber-500 text-black shadow-sm font-extrabold",
          highlight: "text-amber-400",
          border: "border-amber-500/30",
        };
      case "PUNT":
      default:
        return {
          pill: "bg-sky-950/80 border-sky-500/50 text-sky-300 shadow-sky-950/60 shadow-lg",
          badge: "bg-sky-500 text-black shadow-sm font-extrabold",
          highlight: "text-sky-400",
          border: "border-sky-500/30",
        };
    }
  };

  const colors = getActionColor(telemetry.recommendation);
  const netWpFormatted = (telemetry.wpNetGain * 100).toFixed(1);

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`transition-all duration-300 rounded-2xl backdrop-blur-md border p-3 ${colors.pill} ${className}`}
      style={{ minWidth: "280px" }}
    >
      {/* Pill Header Bar */}
      <div className="flex items-center justify-between gap-2 pb-2 border-b border-white/10">
        <div className="flex items-center gap-1.5 text-[10px] font-mono tracking-wider uppercase font-semibold text-slate-300">
          <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
          <span>Baldwin 4th-Down Pill</span>
          {telemetry.isGarbageTime && (
            <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 text-[9px]">
              GARBAGE TIME
            </span>
          )}
        </div>

        {onDismiss && (
          <button
            onClick={onDismiss}
            className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
            title="Dismiss Pill"
          >
            <X className="w-3 h-3" />
          </button>
        )}
      </div>

      {/* Main Recommendation Trigger */}
      <div className="pt-2.5 flex items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span
              className={`px-2.5 py-1 rounded-md text-xs font-mono tracking-wider uppercase ${colors.badge}`}
            >
              {telemetry.recommendation === "GO"
                ? "GO FOR IT"
                : telemetry.recommendation === "FIELD_GOAL"
                  ? "FIELD GOAL"
                  : "PUNT"}
            </span>

            <span className="text-xs font-mono font-bold text-white">+{netWpFormatted}% WP</span>
          </div>

          <div className="text-[11px] text-slate-300 font-mono mt-1">
            4th & {telemetry.yardsToGo} at{" "}
            {telemetry.yardLine > 50
              ? `OPP ${100 - telemetry.yardLine}`
              : `OWN ${telemetry.yardLine}`}
          </div>
        </div>

        {onConfirmRecommendation && (
          <button
            onClick={() => onConfirmRecommendation(telemetry.recommendation)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-mono text-xs font-bold transition-all border border-white/20 active:scale-95 shadow-md"
            title="Press Space or Click to Execute"
          >
            <span>[SPACE]</span>
            <Check className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Expanded Metrics Footer */}
      <div className="mt-2.5 pt-2 border-t border-white/10 grid grid-cols-3 gap-2 text-center font-mono">
        <div className="p-1 rounded bg-black/40 border border-white/5">
          <div className="text-[9px] text-slate-400 uppercase">Conv Odds</div>
          <div className="text-xs font-bold text-emerald-400">
            {Math.round(telemetry.conversionProb * 100)}%
          </div>
        </div>

        <div className="p-1 rounded bg-black/40 border border-white/5">
          <div className="text-[9px] text-slate-400 uppercase">FG Odds</div>
          <div className="text-xs font-bold text-amber-400">
            {Math.round(telemetry.fgMakeProb * 100)}%
          </div>
        </div>

        <div className="p-1 rounded bg-black/40 border border-white/5">
          <div className="text-[9px] text-slate-400 uppercase">Distance</div>
          <div className="text-xs font-bold text-sky-400">{telemetry.fgDistance}y</div>
        </div>
      </div>

      {/* Live Narrative Tip */}
      {isHovered && telemetry.summary && (
        <div className="mt-2 pt-1.5 border-t border-white/10 text-[10px] text-slate-300 font-mono leading-tight">
          {telemetry.summary}
        </div>
      )}
    </div>
  );
};
