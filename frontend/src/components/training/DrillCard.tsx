import type { Drill } from "../../types/training";
import { Zap, Activity, AlertTriangle, TrendingUp } from "lucide-react";

interface DrillCardProps {
  drill: Drill;
  isSelected?: boolean;
  onSelect?: (drill: Drill) => void;
}

export const DrillCard = ({ drill, isSelected = false, onSelect }: DrillCardProps) => {
  const riskColor =
    drill.injuryRisk === "LOW"
      ? "text-emerald-400"
      : drill.injuryRisk === "MEDIUM"
        ? "text-yellow-400"
        : "text-red-500";

  return (
    <div
      onClick={() => onSelect?.(drill)}
      className={`
        relative p-4 rounded-xl border transition-all cursor-pointer group
        ${
          isSelected
            ? "bg-cyan-900/20 border-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.2)]"
            : "bg-white/5 border-white/10 hover:border-white/20 hover:bg-white/10"
        }
      `}
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-white group-hover:text-cyan-300 transition-colors">
          {drill.name}
        </h3>
        <span className="text-[10px] uppercase tracking-wider bg-white/10 px-2 py-0.5 rounded text-gray-300">
          {drill.category}
        </span>
      </div>

      <p className="text-sm text-gray-400 mb-4 h-10 line-clamp-2">{drill.description}</p>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
        <div className="flex items-center gap-1.5 text-gray-300">
          <TrendingUp className="w-3 h-3 text-cyan-400" />
          <span>{drill.targetStats.join(", ")}</span>
        </div>
        <div className="flex items-center gap-1.5 text-gray-300">
          <Zap className="w-3 h-3 text-amber-400" />
          <span>XP x{drill.xpMultiplier}</span>
        </div>
        <div className="flex items-center gap-1.5 text-gray-300">
          <Activity className="w-3 h-3 text-blue-400" />
          <span>Cost: {drill.energyCost}</span>
        </div>
        <div className="flex items-center gap-1.5 text-gray-300">
          <AlertTriangle className={`w-3 h-3 ${riskColor}`} />
          <span className={riskColor}>{drill.injuryRisk} Risk</span>
        </div>
      </div>
    </div>
  );
};
