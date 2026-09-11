import React, { useState } from "react";
import { Clock, Zap, Timer, Flame, ShieldAlert } from "lucide-react";
import { soundEffects } from "../../services/soundEffects";

export type GameTempo = "NORMAL" | "HURRY_UP" | "CHEW_CLOCK";

interface ClockManagementBarProps {
  homeTimeouts?: number;
  awayTimeouts?: number;
  homeTeamName?: string;
  awayTeamName?: string;
  userTeamId?: number;
  isHomeTeam?: boolean;
  currentTempo?: GameTempo;
  onTempoChange?: (tempo: GameTempo) => void;
  onTimeoutCall?: (teamId: number) => void;
  onEmergencyPlay?: (action: "SPIKE" | "KNEEL") => void;
  disabled?: boolean;
}

export const ClockManagementBar: React.FC<ClockManagementBarProps> = ({
  homeTimeouts = 3,
  awayTimeouts = 3,
  homeTeamName = "GB",
  awayTeamName = "CHI",
  userTeamId = 1,
  isHomeTeam = true,
  currentTempo = "NORMAL",
  onTempoChange,
  onTimeoutCall,
  onEmergencyPlay,
  disabled = false,
}) => {
  const [tempo, setTempo] = useState<GameTempo>(currentTempo);
  const [localHomeTimeouts, setLocalHomeTimeouts] = useState<number>(homeTimeouts);
  const [localAwayTimeouts, setLocalAwayTimeouts] = useState<number>(awayTimeouts);

  const activeTimeouts = isHomeTeam ? localHomeTimeouts : localAwayTimeouts;

  const handleTempoSelect = (newTempo: GameTempo) => {
    setTempo(newTempo);
    if (onTempoChange) {
      onTempoChange(newTempo);
    }
  };

  const handleCallTimeout = () => {
    if (disabled || activeTimeouts <= 0) return;
    soundEffects.playWhistle();

    if (isHomeTeam) {
      setLocalHomeTimeouts((prev) => Math.max(0, prev - 1));
    } else {
      setLocalAwayTimeouts((prev) => Math.max(0, prev - 1));
    }

    if (onTimeoutCall) {
      onTimeoutCall(userTeamId);
    }
  };

  const handleSpike = () => {
    if (disabled) return;
    soundEffects.playSnap();
    if (onEmergencyPlay) {
      onEmergencyPlay("SPIKE");
    }
  };

  const handleKneel = () => {
    if (disabled) return;
    soundEffects.playSnap();
    if (onEmergencyPlay) {
      onEmergencyPlay("KNEEL");
    }
  };

  return (
    <div className="w-full bg-slate-900/90 border border-white/10 rounded-xl px-4 py-2.5 backdrop-blur-md flex flex-wrap items-center justify-between gap-4 font-sans text-xs">
      {/* Timeouts Indicator & Call Button */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="font-mono text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
            {isHomeTeam ? homeTeamName : awayTeamName} Timeouts:
          </span>
          <div className="flex items-center gap-1">
            {[1, 2, 3].map((pillIndex) => (
              <div
                key={pillIndex}
                className={`w-3.5 h-3.5 rounded-full transition-all border ${
                  pillIndex <= activeTimeouts
                    ? "bg-amber-400 border-amber-300 shadow-[0_0_8px_rgba(251,191,36,0.6)]"
                    : "bg-slate-800 border-slate-700 opacity-40"
                }`}
                title={`Timeout ${pillIndex}`}
              />
            ))}
          </div>
        </div>

        <button
          onClick={handleCallTimeout}
          disabled={disabled || activeTimeouts <= 0}
          className={`px-3 py-1.5 rounded-lg font-mono font-bold tracking-wider uppercase flex items-center gap-1.5 transition-all ${
            activeTimeouts > 0 && !disabled
              ? "bg-amber-500 hover:bg-amber-400 text-black shadow-md shadow-amber-500/20 active:scale-95 cursor-pointer"
              : "bg-slate-800 text-slate-500 border border-slate-700/50 cursor-not-allowed"
          }`}
        >
          <Clock className="w-3.5 h-3.5" />
          Call Timeout ({activeTimeouts})
        </button>
      </div>

      {/* Clock Tempo Switcher */}
      <div className="flex items-center gap-1 bg-slate-950/70 p-1 rounded-lg border border-white/10">
        <span className="text-[10px] font-mono text-slate-400 px-2 uppercase font-bold">
          Tempo:
        </span>
        <button
          onClick={() => handleTempoSelect("NORMAL")}
          className={`px-2.5 py-1 rounded font-mono font-semibold transition-all ${
            tempo === "NORMAL"
              ? "bg-cyan-500 text-black shadow-sm font-bold"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Standard
        </button>
        <button
          onClick={() => handleTempoSelect("HURRY_UP")}
          className={`px-2.5 py-1 rounded font-mono font-semibold transition-all flex items-center gap-1 ${
            tempo === "HURRY_UP"
              ? "bg-amber-500 text-black shadow-sm font-bold"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <Zap className="w-3 h-3" />
          No-Huddle
        </button>
        <button
          onClick={() => handleTempoSelect("CHEW_CLOCK")}
          className={`px-2.5 py-1 rounded font-mono font-semibold transition-all flex items-center gap-1 ${
            tempo === "CHEW_CLOCK"
              ? "bg-red-500 text-white shadow-sm font-bold"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <Timer className="w-3 h-3" />
          Chew Clock
        </button>
      </div>

      {/* Emergency Clock Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={handleSpike}
          disabled={disabled}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-[11px] font-mono font-bold uppercase tracking-wider flex items-center gap-1 transition-all active:scale-95 disabled:opacity-50"
          title="Spike the ball to stop clock on next down"
        >
          <Flame className="w-3.5 h-3.5 text-amber-400" />
          Spike
        </button>
        <button
          onClick={handleKneel}
          disabled={disabled}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-[11px] font-mono font-bold uppercase tracking-wider flex items-center gap-1 transition-all active:scale-95 disabled:opacity-50"
          title="Victory formation kneel to bleed clock"
        >
          <ShieldAlert className="w-3.5 h-3.5 text-cyan-400" />
          Victory Kneel
        </button>
      </div>
    </div>
  );
};
