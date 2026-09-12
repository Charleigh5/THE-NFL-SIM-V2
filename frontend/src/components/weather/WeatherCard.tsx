import React from "react";
import { useWeatherThemeStore } from "../../store/useWeatherThemeStore";

interface WeatherCardProps {
  children: React.ReactNode;
  className?: string;
  glow?: "cyan" | "pink" | "amber" | "none";
  title?: string;
  badge?: string;
}

export const WeatherCard: React.FC<WeatherCardProps> = ({
  children,
  className = "",
  glow = "cyan",
  title,
  badge,
}) => {
  const { condition, lightningActive } = useWeatherThemeStore();

  const isBlizzard = condition === "LAMBEAU_BLIZZARD";
  const isRain = condition === "ARROWHEAD_DOWNPOUR";
  const isVice = condition === "VICE_HEATWAVE";

  const getGlowBorder = () => {
    switch (glow) {
      case "pink":
        return "border-pink-500/40 shadow-[0_0_15px_rgba(255,20,147,0.15)]";
      case "amber":
        return "border-amber-500/40 shadow-[0_0_15px_rgba(255,184,0,0.15)]";
      case "none":
        return "border-neutral-800";
      case "cyan":
      default:
        return "border-cyan-500/30 shadow-[0_0_15px_rgba(0,240,255,0.12)]";
    }
  };

  return (
    <div
      data-weather-surface="true"
      className={`relative rounded-lg border bg-neutral-950/80 backdrop-blur-xl transition-all duration-300 ${getGlowBorder()} ${
        isBlizzard ? "border-t-cyan-200/50" : ""
      } ${isRain ? "border-b-blue-400/30" : ""} ${
        isVice ? "shadow-[0_0_25px_rgba(255,20,147,0.2)]" : ""
      } ${lightningActive ? "brightness-125 border-white/60" : ""} ${className}`}
    >
      {/* Header bar if title provided */}
      {(title || badge) && (
        <div className="flex items-center justify-between px-4 py-2.5 border-b border-neutral-800/80 bg-neutral-900/40">
          {title && (
            <h3 className="font-mono text-xs font-bold uppercase tracking-wider text-neutral-200">
              {title}
            </h3>
          )}
          {badge && (
            <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-cyan-950/80 text-cyan-300 border border-cyan-500/30">
              {badge}
            </span>
          )}
        </div>
      )}

      {/* Card Body */}
      <div className="p-4">{children}</div>
    </div>
  );
};
