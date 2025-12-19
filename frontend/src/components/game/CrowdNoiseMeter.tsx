import React from "react";
import { Volume2, MicOff, AlertCircle } from "lucide-react";
import "./CrowdNoiseMeter.css";

export type CrowdNoiseLevel = "QUIET" | "MODERATE" | "LOUD" | "DEAFENING";

interface CrowdNoiseMeterProps {
  decibels: number; // 50 to 120
  stadiumName?: string;
  isAwayTeamOnOffense: boolean;
}

export const CrowdNoiseMeter: React.FC<CrowdNoiseMeterProps> = ({
  decibels,
  stadiumName = "Stadium",
  isAwayTeamOnOffense,
}) => {
  let level: CrowdNoiseLevel = "QUIET";
  if (decibels >= 105) level = "DEAFENING";
  else if (decibels >= 90) level = "LOUD";
  else if (decibels >= 75) level = "MODERATE";

  // Visual config based on level
  const config = {
    QUIET: {
      color: "text-blue-400",
      barColor: "bg-blue-500",
      icon: Volume2,
      label: "Low Noise",
      effect: "No impact on communication.",
    },
    MODERATE: {
      color: "text-green-400",
      barColor: "bg-green-500",
      icon: Volume2,
      label: "Standard Crowd",
      effect: "Normal game conditions.",
    },
    LOUD: {
      color: "text-orange-400",
      barColor: "bg-orange-500",
      icon: AlertCircle,
      label: "High Decibels",
      effect: "Communication strained. Check audibles.",
    },
    DEAFENING: {
      color: "text-red-500",
      animate: "animate-pulse",
      barColor: "bg-red-600",
      icon: MicOff,
      label: "DEAFENING",
      effect: "Verbal communication impossible. False start risk HIGH.",
    },
  };

  const currentConfig = config[level];
  const Icon = currentConfig.icon;

  // Calculate meter fill (clamp between 0 and 100 based on 50db-120db range)
  // 50db = 0%, 120db = 100%
  const fillPercentage = Math.min(100, Math.max(0, ((decibels - 60) / 60) * 100));

  return (
    <div className="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-4 w-full max-w-xs transition-all duration-500">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Icon
            className={`w-5 h-5 ${currentConfig.color} ${level === "DEAFENING" ? "animate-bounce" : ""}`}
          />
          <span className={`font-bold font-anton tracking-wide text-lg ${currentConfig.color}`}>
            {decibels.toFixed(0)} dB
          </span>
        </div>
        <span className="text-white/50 text-xs uppercase font-medium tracking-wider">
          {stadiumName}
        </span>
      </div>

      {/* Meter Bar */}
      <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden mb-3 shadow-inner">
        <div
          className={`meter-fill-bar h-full ${currentConfig.barColor} ${
            level === "DEAFENING" ? "animate-pulse" : ""
          }`}
          style={{ "--fill-width": `${fillPercentage}%` } as React.CSSProperties}
        />
      </div>

      <div className="flex flex-col gap-1">
        <span className={`text-sm font-bold uppercase ${currentConfig.color}`}>
          {currentConfig.label}
        </span>
        <p className="text-xs text-white/70 leading-relaxed">
          {isAwayTeamOnOffense && level !== "QUIET"
            ? currentConfig.effect
            : "Home team unaffected."}
        </p>
      </div>
    </div>
  );
};
