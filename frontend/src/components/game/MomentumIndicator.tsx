import { Flame, Snowflake, Minus, ChevronUp } from "lucide-react";
import { MomentumState } from "../../types/momentum";

interface MomentumIndicatorProps {
  label: string;
  state: MomentumState;
  align?: "left" | "right";
}

export const MomentumIndicator = ({ label, state, align = "left" }: MomentumIndicatorProps) => {
  const getConfig = (s: MomentumState) => {
    switch (s) {
      case MomentumState.ON_FIRE:
        return {
          color: "text-amber-400",
          bg: "bg-amber-500/20",
          border: "border-amber-500/50",
          icon: <Flame className="w-4 h-4 animate-pulse" fill="currentColor" />,
          text: "ON FIRE",
          shadow: "shadow-[0_0_15px_rgba(251,191,36,0.5)]",
        };
      case MomentumState.HEATING_UP:
        return {
          color: "text-orange-400",
          bg: "bg-orange-500/20",
          border: "border-orange-500/50",
          icon: <ChevronUp className="w-4 h-4" />,
          text: "HEATING UP",
          shadow: "shadow-[0_0_10px_rgba(251,146,60,0.3)]",
        };
      case MomentumState.COLD:
        return {
          color: "text-blue-400",
          bg: "bg-blue-500/20",
          border: "border-blue-500/50",
          icon: <Snowflake className="w-4 h-4" />,
          text: "COLD",
          shadow: "",
        };
      case MomentumState.ICE_COLD:
        return {
          color: "text-cyan-300",
          bg: "bg-cyan-500/20",
          border: "border-cyan-500/50",
          icon: <Snowflake className="w-4 h-4 animate-spin-slow" />,
          text: "ICE COLD",
          shadow: "shadow-[0_0_10px_rgba(34,211,238,0.3)]",
        };
      default:
        return {
          color: "text-gray-400",
          bg: "bg-white/5",
          border: "border-white/10",
          icon: <Minus className="w-4 h-4" />,
          text: "NEUTRAL",
          shadow: "",
        };
    }
  };

  const config = getConfig(state);

  return (
    <div className={`flex flex-col gap-1 ${align === "right" ? "items-end" : "items-start"}`}>
      <span className="text-[10px] uppercase tracking-wider text-gray-500 font-bold">{label}</span>
      <div
        className={`flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all duration-500 ${config.bg} ${config.border} ${config.shadow}`}
      >
        <div className={`${config.color}`}>{config.icon}</div>
        <span className={`text-xs font-bold tracking-wide ${config.color}`}>{config.text}</span>
      </div>
    </div>
  );
};
