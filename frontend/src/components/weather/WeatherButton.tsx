import React from "react";
import { useWeatherThemeStore } from "../../store/useWeatherThemeStore";

interface WeatherButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost" | "gold";
  children: React.ReactNode;
  className?: string;
}

export const WeatherButton: React.FC<WeatherButtonProps> = ({
  variant = "primary",
  children,
  className = "",
  ...props
}) => {
  const { condition, lightningActive } = useWeatherThemeStore();

  const isBlizzard = condition === "LAMBEAU_BLIZZARD";
  const isRain = condition === "ARROWHEAD_DOWNPOUR";
  const isVice = condition === "VICE_HEATWAVE";

  const getVariantStyles = () => {
    switch (variant) {
      case "danger":
        return "bg-rose-950/70 hover:bg-rose-900 border-rose-500/50 text-rose-200 shadow-[0_0_12px_rgba(244,63,94,0.3)]";
      case "gold":
        return "bg-amber-950/70 hover:bg-amber-900 border-amber-400/60 text-amber-200 shadow-[0_0_12px_rgba(251,191,36,0.3)]";
      case "secondary":
        return "bg-neutral-900/80 hover:bg-neutral-800 border-neutral-700 text-neutral-200";
      case "ghost":
        return "bg-transparent hover:bg-white/5 border-transparent text-neutral-400 hover:text-white";
      case "primary":
      default:
        return "bg-cyan-950/70 hover:bg-cyan-900/90 border-cyan-400/60 text-cyan-200 shadow-[0_0_15px_rgba(0,240,255,0.25)]";
    }
  };

  return (
    <button
      data-weather-surface="true"
      className={`relative group px-4 py-2 rounded font-mono text-xs uppercase tracking-wider font-semibold border transition-all duration-200 active:scale-95 select-none ${getVariantStyles()} ${
        isBlizzard ? "shadow-[inset_0_2px_4px_rgba(255,255,255,0.4)]" : ""
      } ${isRain ? "backdrop-blur-md" : ""} ${
        isVice ? "hover:shadow-[0_0_20px_rgba(255,20,147,0.5)]" : ""
      } ${lightningActive ? "brightness-150 contrast-125" : ""} ${className}`}
      {...props}
    >
      {/* Subtle frost corner indicator in winter */}
      {isBlizzard && (
        <span className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 bg-white rounded-full opacity-80 pointer-events-none shadow-[0_0_4px_#fff]" />
      )}

      {/* Glossy wet specular reflection line in rain */}
      {isRain && (
        <span className="absolute inset-x-2 top-0.5 h-0.5 bg-gradient-to-r from-transparent via-cyan-200/40 to-transparent pointer-events-none" />
      )}

      {children}
    </button>
  );
};
