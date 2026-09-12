import React, { useState } from "react";
import {
  CloudSnow,
  CloudRain,
  Sun,
  Wind,
  Zap,
  ShieldAlert,
  Flame,
  Activity,
  Layers,
  Sparkles,
  Award,
  Crosshair,
} from "lucide-react";
import {
  useWeatherThemeStore,
  WEATHER_PRESETS,
  type WeatherCondition,
} from "../store/useWeatherThemeStore";
import { WeatherButton } from "../components/weather/WeatherButton";
import { WeatherCard } from "../components/weather/WeatherCard";
import { weatherAudio } from "../services/weatherAudioService";

export const EnvironmentalWeatherLab: React.FC = () => {
  const {
    condition,
    preset,
    lightningActive,
    setCondition,
    triggerLightning,
    toggle3DBackdrop,
    show3DBackdrop,
    audioEnabled,
    toggleAudio,
  } = useWeatherThemeStore();

  const [simulatedScore, setSimulatedScore] = useState({ home: 24, away: 21 });
  const [playActionLog, setPlayActionLog] = useState<string[]>([
    "System Initialized: Dynamic Weather & Season FX Active",
    `Current Stadium: ${preset.location} (${preset.temperature}°F)`,
  ]);

  const recordAction = (action: string) => {
    setPlayActionLog((prev) => [
      `[${new Date().toLocaleTimeString()}] ${action}`,
      ...prev.slice(0, 5),
    ]);
  };

  const handlePlayCall = (playName: string) => {
    recordAction(`Audible Executed: ${playName}`);
    triggerLightning(0.6);
    if (audioEnabled) {
      weatherAudio.playThunderStrike(0.5);
    }
  };

  const handleScoreUpdate = () => {
    setSimulatedScore((prev) => ({ ...prev, home: prev.home + 7 }));
    recordAction("TOUCHDOWN MIAMI! Stadium lights surging!");
    triggerLightning(1.4);
    if (audioEnabled) {
      weatherAudio.playThunderStrike(1.2);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16 font-sans">
      {/* Broadcast Header HUD */}
      <div className="relative overflow-hidden rounded-xl border border-cyan-500/40 bg-neutral-950/85 backdrop-blur-2xl p-6 shadow-2xl shadow-cyan-950/40">
        <div className="absolute top-0 right-0 p-4 opacity-10 font-mono text-8xl font-black select-none pointer-events-none text-cyan-400">
          AAAA-FX
        </div>

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded bg-pink-950/80 border border-pink-500/50 text-pink-300 font-mono text-[10px] font-bold tracking-widest uppercase">
                MADDEN 25 × GTA 6 ENGINE
              </span>
              <span className="text-neutral-400 font-mono text-xs">
                • 60Hz PBR ENVIRONMENTAL LAB
              </span>
            </div>
            <h1 className="font-heading text-4xl lg:text-5xl font-black uppercase tracking-tight text-white flex items-center gap-3">
              PHOTOREALISTIC SEASONS & WEATHER FX
            </h1>
            <p className="text-neutral-400 text-sm mt-1 max-w-2xl font-mono">
              Live multi-season physical simulation. Watch snow accumulate on buttons, water
              droplets drip off cards, volumetric thunder bolts illuminate the stadium, and 3D PBR
              turf react dynamically to environmental physics.
            </p>
          </div>

          {/* Stadium Selector Pills */}
          <div className="flex flex-wrap lg:flex-nowrap gap-2">
            {(Object.keys(WEATHER_PRESETS) as WeatherCondition[]).map((key) => {
              const p = WEATHER_PRESETS[key];
              const isSelected = condition === key;
              return (
                <button
                  key={key}
                  onClick={() => {
                    setCondition(key);
                    recordAction(`Shifted Stadium Season: ${p.name}`);
                  }}
                  data-weather-surface="true"
                  className={`px-3 py-2 rounded-lg font-mono text-xs font-bold transition-all flex items-center gap-2 border ${
                    isSelected
                      ? "bg-cyan-500/20 border-cyan-400 text-cyan-300 shadow-[0_0_15px_rgba(0,240,255,0.3)] scale-105"
                      : "bg-neutral-900/60 border-neutral-800 text-neutral-400 hover:text-neutral-200"
                  }`}
                >
                  {key === "LAMBEAU_BLIZZARD" && (
                    <CloudSnow className="w-3.5 h-3.5 text-cyan-200" />
                  )}
                  {key === "ARROWHEAD_DOWNPOUR" && (
                    <CloudRain className="w-3.5 h-3.5 text-blue-400" />
                  )}
                  {key === "VICE_HEATWAVE" && <Sun className="w-3.5 h-3.5 text-pink-500" />}
                  {key === "FOXBOROUGH_AUTUMN" && <Wind className="w-3.5 h-3.5 text-amber-400" />}
                  {key === "CLEAR_NIGHT" && <Sparkles className="w-3.5 h-3.5 text-cyan-400" />}
                  <span>{p.name.split(" ")[0]}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Grid of Interactive Modules */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Module 1: Interactive Snow-Capped Tactile Play-Calling Deck */}
        <WeatherCard
          title="Tactile Coach Playbook HUD"
          badge="COLLISION DETECTED"
          glow="cyan"
          className="lg:col-span-2"
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <p className="text-xs text-neutral-400 font-mono">
                Hover or click buttons below to physically dislodge accumulated snow caps into
                airborne powder particles.
              </p>
              <span className="text-[11px] font-mono text-cyan-400">
                TEMP: {preset.temperature}°F // TURF: {preset.turfTint}
              </span>
            </div>

            {/* Interactive Button Rack */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
              <WeatherButton
                variant="primary"
                onClick={() => handlePlayCall("GUN TRIPS - MIAMI VERTICALS")}
              >
                <div className="flex flex-col items-center gap-1 py-1">
                  <Crosshair className="w-4 h-4 text-cyan-300" />
                  <span>Miami Verticals</span>
                  <span className="text-[9px] opacity-70">Pass • +14 Yds</span>
                </div>
              </WeatherButton>

              <WeatherButton
                variant="danger"
                onClick={() => handlePlayCall("DOUBLE A-GAP BLITZ 0")}
              >
                <div className="flex flex-col items-center gap-1 py-1">
                  <ShieldAlert className="w-4 h-4 text-rose-300" />
                  <span>Cover 0 Blitz</span>
                  <span className="text-[9px] opacity-70">Def • Heavy Rush</span>
                </div>
              </WeatherButton>

              <WeatherButton variant="gold" onClick={() => handlePlayCall("PISTOL POWER RUN")}>
                <div className="flex flex-col items-center gap-1 py-1">
                  <Flame className="w-4 h-4 text-amber-300" />
                  <span>Pistol Power</span>
                  <span className="text-[9px] opacity-70">Run • Off-Tackle</span>
                </div>
              </WeatherButton>

              <WeatherButton variant="secondary" onClick={handleScoreUpdate}>
                <div className="flex flex-col items-center gap-1 py-1">
                  <Award className="w-4 h-4 text-emerald-400" />
                  <span>Score Touchdown</span>
                  <span className="text-[9px] opacity-70">Lightning Surge</span>
                </div>
              </WeatherButton>
            </div>

            {/* Live Telemetry & Event Log */}
            <div className="rounded-md bg-neutral-950/90 border border-neutral-800 p-3 font-mono text-xs space-y-1">
              <div className="flex justify-between text-neutral-400 border-b border-neutral-800 pb-1 mb-1 text-[11px]">
                <span>LIVE TELEMETRY STREAM</span>
                <span className="text-cyan-400 font-bold">
                  {simulatedScore.home} - {simulatedScore.away}
                </span>
              </div>
              {playActionLog.map((log, idx) => (
                <div key={idx} className="text-[11px] text-neutral-300 truncate">
                  {log}
                </div>
              ))}
            </div>
          </div>
        </WeatherCard>

        {/* Module 2: Atmospheric Environmental Sensors */}
        <WeatherCard title="Stadium Meteorological Telemetry" badge="NEXT-GEN SENSORS" glow="pink">
          <div className="space-y-3 font-mono text-xs">
            <div className="p-3 bg-neutral-900/60 rounded border border-neutral-800 space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-neutral-400">SURFACE TURF FRICTION:</span>
                <span className="text-cyan-400 font-bold">
                  {condition === "LAMBEAU_BLIZZARD"
                    ? "μ = 0.42 (SLIP HAZARD)"
                    : condition === "ARROWHEAD_DOWNPOUR"
                      ? "μ = 0.58 (SLICK)"
                      : "μ = 0.88 (OPTIMAL)"}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neutral-400">WIND VECTOR:</span>
                <span className="text-amber-400 font-bold">
                  {preset.windSpeed} MPH ({(preset.windAngleRad * (180 / Math.PI)).toFixed(0)}° SSE)
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neutral-400">AIR VISCOSITY INDEX:</span>
                <span className="text-pink-400 font-bold">
                  {condition === "VICE_HEATWAVE" ? "89% HUMID (HEAVY)" : "12% DENSE (SUB-ZERO)"}
                </span>
              </div>
            </div>

            <div className="space-y-2 pt-1">
              <button
                onClick={() => triggerLightning(1.2)}
                data-weather-surface="true"
                className="w-full py-2 bg-gradient-to-r from-pink-900/80 to-purple-900/80 hover:from-pink-800 hover:to-purple-800 border border-pink-500/50 rounded font-bold text-white uppercase tracking-wider flex items-center justify-center gap-2 transition-all active:scale-98"
              >
                <Zap className="w-4 h-4 text-pink-400 animate-pulse" />
                Trigger Thunder Strike
              </button>

              <button
                onClick={toggle3DBackdrop}
                data-weather-surface="true"
                className="w-full py-2 bg-neutral-900 hover:bg-neutral-800 border border-neutral-700 rounded font-bold text-neutral-300 uppercase tracking-wider flex items-center justify-center gap-2 transition-all"
              >
                <Layers className="w-4 h-4 text-purple-400" />
                3D Stadium Viewport: {show3DBackdrop ? "Active" : "Disabled"}
              </button>

              <button
                onClick={toggleAudio}
                data-weather-surface="true"
                className="w-full py-2 bg-neutral-900 hover:bg-neutral-800 border border-neutral-700 rounded font-bold text-neutral-300 uppercase tracking-wider flex items-center justify-center gap-2 transition-all"
              >
                <Activity className="w-4 h-4 text-cyan-400" />
                Procedural Soundscape: {audioEnabled ? "Enabled" : "Muted"}
              </button>
            </div>
          </div>
        </WeatherCard>
      </div>

      {/* Lightning indicator banner when strike is live */}
      {lightningActive && (
        <div className="p-3 bg-cyan-950/80 border border-cyan-400 rounded-lg text-center font-mono text-cyan-200 text-xs tracking-widest uppercase animate-pulse">
          ⚡ VOLUMETRIC LIGHTNING SURGE DETECTED // STADIUM FLOODLIGHTS COMPENSATING
        </div>
      )}
    </div>
  );
};
