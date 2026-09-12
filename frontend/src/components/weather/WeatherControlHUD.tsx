import React, { useState } from "react";
import {
  CloudRain,
  CloudSnow,
  Sun,
  Wind,
  Zap,
  Volume2,
  VolumeX,
  Layers,
  Sparkles,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import {
  useWeatherThemeStore,
  WEATHER_PRESETS,
  type WeatherCondition,
} from "../../store/useWeatherThemeStore";
import { weatherAudio } from "../../services/weatherAudioService";

export const WeatherControlHUD: React.FC = () => {
  const {
    condition,
    preset,
    show3DBackdrop,
    snowAccumulationActive,
    audioEnabled,
    setCondition,
    triggerLightning,
    toggle3DBackdrop,
    toggleSnowAccumulation,
    toggleAudio,
  } = useWeatherThemeStore();

  const [isExpanded, setIsExpanded] = useState(false);

  const handleLightning = () => {
    triggerLightning(1.2);
    if (audioEnabled) {
      weatherAudio.playThunderStrike(1.0);
    }
  };

  const getConditionIcon = (cond: WeatherCondition) => {
    switch (cond) {
      case "LAMBEAU_BLIZZARD":
        return <CloudSnow className="w-4 h-4 text-cyan-300 animate-pulse" />;
      case "ARROWHEAD_DOWNPOUR":
        return <CloudRain className="w-4 h-4 text-blue-400 animate-pulse" />;
      case "VICE_HEATWAVE":
        return <Sun className="w-4 h-4 text-pink-500 animate-spin" />;
      case "FOXBOROUGH_AUTUMN":
        return <Wind className="w-4 h-4 text-amber-400" />;
      case "CLEAR_NIGHT":
      default:
        return <Sparkles className="w-4 h-4 text-cyan-400" />;
    }
  };

  return (
    <aside
      aria-label="Environmental Weather Console"
      className="fixed bottom-4 right-4 z-40 flex flex-col items-end pointer-events-auto"
    >
      {/* Expanded Controls Panel */}
      {isExpanded && (
        <div className="mb-2 w-80 bg-neutral-950/90 backdrop-blur-xl border border-cyan-500/40 rounded-lg p-3 shadow-2xl shadow-cyan-950/50 text-white font-mono text-xs">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-cyan-500/20 pb-2 mb-3">
            <div className="flex items-center gap-2">
              <Zap className="w-3.5 h-3.5 text-cyan-400" />
              <span className="font-bold tracking-wider uppercase text-cyan-400">
                DYNAMIC WEATHER FX // AAAA
              </span>
            </div>
            <span className="text-[10px] text-neutral-400 font-sans">{preset.seasonLabel}</span>
          </div>

          {/* Location & Conditions */}
          <div className="bg-neutral-900/80 rounded p-2 mb-3 border border-neutral-800">
            <div className="flex justify-between items-center mb-1">
              <span className="text-neutral-400 text-[11px]">{preset.location}</span>
              <span className="text-amber-400 font-bold">{preset.temperature}°F</span>
            </div>
            <div className="text-[10px] text-neutral-300 italic mb-1.5">{preset.description}</div>
            <div className="flex items-center justify-between text-[10px] text-cyan-300/80">
              <span>WIND: {preset.windSpeed} MPH</span>
              <span>PARTICLES: {Math.round(preset.precipitationDensity * 100)}%</span>
            </div>
          </div>

          {/* Condition Selectors */}
          <div className="space-y-1 mb-3">
            <label className="text-[10px] uppercase text-neutral-400 tracking-wider">
              Select Stadium Environment:
            </label>
            <div className="grid grid-cols-1 gap-1">
              {(Object.keys(WEATHER_PRESETS) as WeatherCondition[]).map((key) => {
                const p = WEATHER_PRESETS[key];
                const isActive = condition === key;
                return (
                  <button
                    key={key}
                    onClick={() => setCondition(key)}
                    data-weather-surface="true"
                    className={`flex items-center justify-between px-2.5 py-1.5 rounded transition-all text-left ${
                      isActive
                        ? "bg-cyan-500/20 border border-cyan-400 text-cyan-300 shadow-[0_0_10px_rgba(0,240,255,0.2)]"
                        : "bg-neutral-900/50 hover:bg-neutral-800 border border-neutral-800 text-neutral-300"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {getConditionIcon(key)}
                      <span className="font-sans font-semibold text-[11px]">{p.name}</span>
                    </div>
                    <span className="text-[10px] opacity-75">{p.temperature}°F</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Quick Action Triggers */}
          <div className="grid grid-cols-2 gap-1.5 pt-1 border-t border-neutral-800/80">
            <button
              onClick={handleLightning}
              data-weather-surface="true"
              className="flex items-center justify-center gap-1.5 py-1.5 px-2 bg-pink-950/60 hover:bg-pink-900/80 border border-pink-500/50 rounded text-pink-300 font-bold text-[10px] uppercase tracking-wider transition-all"
            >
              <Zap className="w-3 h-3 text-pink-400 animate-bounce" />
              Lightning Bolt
            </button>

            <button
              onClick={toggleAudio}
              data-weather-surface="true"
              className={`flex items-center justify-center gap-1.5 py-1.5 px-2 border rounded font-bold text-[10px] uppercase tracking-wider transition-all ${
                audioEnabled
                  ? "bg-cyan-950/60 border-cyan-400 text-cyan-300"
                  : "bg-neutral-900 hover:bg-neutral-800 border-neutral-800 text-neutral-400"
              }`}
            >
              {audioEnabled ? (
                <>
                  <Volume2 className="w-3 h-3 text-cyan-400" />
                  Audio: Live
                </>
              ) : (
                <>
                  <VolumeX className="w-3 h-3" />
                  Audio: Muted
                </>
              )}
            </button>

            <button
              onClick={toggle3DBackdrop}
              data-weather-surface="true"
              className={`flex items-center justify-center gap-1.5 py-1.5 px-2 border rounded font-bold text-[10px] uppercase tracking-wider transition-all ${
                show3DBackdrop
                  ? "bg-purple-950/60 border-purple-400 text-purple-300"
                  : "bg-neutral-900 hover:bg-neutral-800 border-neutral-800 text-neutral-400"
              }`}
            >
              <Layers className="w-3 h-3" />
              3D Stadium: {show3DBackdrop ? "ON" : "OFF"}
            </button>

            <button
              onClick={toggleSnowAccumulation}
              data-weather-surface="true"
              className={`flex items-center justify-center gap-1.5 py-1.5 px-2 border rounded font-bold text-[10px] uppercase tracking-wider transition-all ${
                snowAccumulationActive
                  ? "bg-blue-950/60 border-blue-400 text-blue-300"
                  : "bg-neutral-900 hover:bg-neutral-800 border-neutral-800 text-neutral-400"
              }`}
            >
              <CloudSnow className="w-3 h-3" />
              Snow Accum: {snowAccumulationActive ? "ON" : "OFF"}
            </button>
          </div>
        </div>
      )}

      {/* Floating Pill Toggle Button */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        data-weather-surface="true"
        className="flex items-center gap-2 px-3 py-2 bg-neutral-950/90 hover:bg-neutral-900 border border-cyan-500/50 rounded-full shadow-lg shadow-cyan-950/80 text-white transition-all transform hover:scale-105"
      >
        <div className="flex items-center gap-1.5">
          {getConditionIcon(condition)}
          <span className="font-mono text-xs font-bold text-cyan-300">{preset.temperature}°F</span>
        </div>
        <span className="text-[11px] font-sans font-medium text-neutral-300 hidden sm:inline">
          {preset.name}
        </span>
        {isExpanded ? (
          <ChevronDown className="w-3.5 h-3.5 text-cyan-400" />
        ) : (
          <ChevronUp className="w-3.5 h-3.5 text-cyan-400" />
        )}
      </button>
    </aside>
  );
};
