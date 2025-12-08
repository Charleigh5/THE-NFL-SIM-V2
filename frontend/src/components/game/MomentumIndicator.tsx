import { MomentumState } from "../../types/momentum";
import { Flame, Snowflake, Minus } from "lucide-react";

interface MomentumIndicatorProps {
  state: MomentumState;
  size?: "sm" | "md";
}

export const MomentumIndicator = ({ state, size = "md" }: MomentumIndicatorProps) => {
  const getStyle = () => {
    switch (state) {
      case MomentumState.ICE_COLD:
        return {
          icon: Snowflake,
          color: "text-blue-400",
          bg: "bg-blue-400/10",
          border: "border-blue-400/20",
          label: "Ice Cold",
          animate: "animate-pulse",
        };
      case MomentumState.COLD:
        return {
          icon: Snowflake,
          color: "text-cyan-300",
          bg: "bg-cyan-300/5",
          border: "border-cyan-300/10",
          label: "Cold",
          animate: "",
        };
      case MomentumState.HEATING_UP:
        return {
          icon: Flame,
          color: "text-orange-400",
          bg: "bg-orange-400/10",
          border: "border-orange-400/20",
          label: "Heating Up",
          animate: "animate-pulse",
        };
      case MomentumState.ON_FIRE:
        return {
          icon: Flame,
          color: "text-amber-400",
          bg: "bg-amber-400/10",
          border: "border-amber-400/20",
          label: "On Fire",
          animate: "animate-bounce", // Subtle bounce or aggressive pulse
        };
      default:
        return {
          icon: Minus,
          color: "text-gray-500",
          bg: "bg-gray-500/5",
          border: "border-gray-500/10",
          label: "Neutral",
          animate: "",
        };
    }
  };

  const style = getStyle();
  const Icon = style.icon;

  return (
    <div
      className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full border ${style.bg} ${style.border}`}
      title={`Momentum: ${style.label}`}
    >
      <Icon className={`w-3 h-3 ${style.color} ${style.animate}`} />
      {size === "md" && (
        <span className={`text-[10px] uppercase tracking-wider font-bold ${style.color}`}>
          {style.label}
        </span>
      )}
    </div>
  );
};
