import React, { useState, useEffect } from "react";
import { soundEffects } from "../../services/soundEffects";
import type { SpatialAudioConfig } from "../../services/soundEffects";
import {
  Volume2,
  VolumeX,
  Radio,
  Users,
  Sparkles,
  X,
  Play,
  CheckCircle,
  Sliders,
} from "lucide-react";

interface SpatialAudioSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SpatialAudioSettingsModal: React.FC<SpatialAudioSettingsModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [config, setConfig] = useState<SpatialAudioConfig>(() => soundEffects.getConfig());
  const [lastAuditioned, setLastAuditioned] = useState<string | null>(null);

  // Sync state if modal opens
  useEffect(() => {
    if (isOpen) {
      setConfig(soundEffects.getConfig());
    }
  }, [isOpen]);

  // Handle ESC key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVol = parseFloat(e.target.value);
    soundEffects.setVolume(newVol);
    setConfig((prev) => ({ ...prev, volume: newVol }));
  };

  const handleToggleMute = () => {
    const nextMute = !config.isMuted;
    soundEffects.setMuted(nextMute);
    setConfig((prev) => ({ ...prev, isMuted: nextMute }));
    if (!nextMute) {
      soundEffects.playSnap();
    }
  };

  const handleToggleSpatial = () => {
    const nextVal = !config.spatialAudioEnabled;
    soundEffects.setSpatialAudioEnabled(nextVal);
    setConfig((prev) => ({ ...prev, spatialAudioEnabled: nextVal }));
    soundEffects.playSnap();
  };

  const handleToggleCrowd = () => {
    const nextVal = !config.crowdEnabled;
    soundEffects.setCrowdEnabled(nextVal);
    setConfig((prev) => ({ ...prev, crowdEnabled: nextVal }));
    soundEffects.playSnap();
  };

  const handleToggleSfx = () => {
    const nextVal = !config.sfxEnabled;
    soundEffects.setSfxEnabled(nextVal);
    setConfig((prev) => ({ ...prev, sfxEnabled: nextVal }));
    soundEffects.playSnap();
  };

  const runAudition = (label: string, action: () => void) => {
    setLastAuditioned(label);
    action();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div
        className="relative w-full max-w-xl bg-gray-950/95 border border-white/15 rounded-2xl shadow-2xl overflow-hidden font-body text-white"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-white/5">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              <Radio className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-header uppercase tracking-wider text-white">
                Spatial Audio & Soundscape Settings
              </h2>
              <p className="text-xs text-gray-400 font-mono">
                100% Procedural Web Audio API Synthesis • Zero External Downloads
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
            aria-label="Close Settings"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
          {/* Master Volume Section */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sliders className="w-4 h-4 text-emerald-400" />
                <span className="text-sm font-semibold uppercase tracking-wide">Master Volume</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-gray-300">
                  {config.isMuted ? "MUTED" : `${Math.round(config.volume * 100)}%`}
                </span>
                <button
                  onClick={handleToggleMute}
                  className={`p-1.5 rounded-lg text-xs font-mono transition-colors ${
                    config.isMuted
                      ? "bg-red-500/20 text-red-400 border border-red-500/40"
                      : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                  }`}
                  aria-label={config.isMuted ? "Unmute Audio" : "Mute Audio"}
                >
                  {config.isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={config.volume}
              onChange={handleVolumeChange}
              disabled={config.isMuted}
              className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-emerald-500 disabled:opacity-40"
              aria-label="Master volume slider"
            />
          </div>

          {/* Spatial 2D Stereo Panning Section */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Radio className="w-4 h-4 text-cyan-400" />
                <div>
                  <span className="text-sm font-semibold uppercase tracking-wide">
                    2D Spatial Stereo Panning
                  </span>
                  <p className="text-xs text-gray-400">
                    Pans field collisions and whistles across stereo channels by yardline [0, 120].
                  </p>
                </div>
              </div>
              <button
                onClick={handleToggleSpatial}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  config.spatialAudioEnabled ? "bg-cyan-600" : "bg-gray-800"
                }`}
                role="switch"
                aria-checked={config.spatialAudioEnabled}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    config.spatialAudioEnabled ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            {/* Spatial Field Audition Buttons */}
            <div className="pt-2 border-t border-white/5">
              <span className="text-[11px] font-mono text-gray-400 uppercase tracking-wider block mb-2">
                Audition Spatial Collision (Stereo Spread):
              </span>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() =>
                    runAudition("Left Endzone Hit", () => soundEffects.playSpatialHit(10, 26.65, 1400))
                  }
                  className="px-2.5 py-1.5 rounded-lg text-xs font-mono bg-cyan-950/60 hover:bg-cyan-900/60 border border-cyan-500/30 text-cyan-200 transition-colors flex items-center justify-center gap-1.5"
                >
                  <Play className="w-3 h-3" />
                  Left (Pan -0.7)
                </button>
                <button
                  onClick={() =>
                    runAudition("Midfield Hit", () => soundEffects.playSpatialHit(60, 26.65, 1400))
                  }
                  className="px-2.5 py-1.5 rounded-lg text-xs font-mono bg-cyan-950/60 hover:bg-cyan-900/60 border border-cyan-500/30 text-cyan-200 transition-colors flex items-center justify-center gap-1.5"
                >
                  <Play className="w-3 h-3" />
                  Center (Pan 0.0)
                </button>
                <button
                  onClick={() =>
                    runAudition("Right Endzone Hit", () => soundEffects.playSpatialHit(110, 26.65, 1400))
                  }
                  className="px-2.5 py-1.5 rounded-lg text-xs font-mono bg-cyan-950/60 hover:bg-cyan-900/60 border border-cyan-500/30 text-cyan-200 transition-colors flex items-center justify-center gap-1.5"
                >
                  <Play className="w-3 h-3" />
                  Right (Pan +0.7)
                </button>
              </div>
            </div>
          </div>

          {/* Procedural Crowd Ambience Section */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-amber-400" />
                <div>
                  <span className="text-sm font-semibold uppercase tracking-wide">
                    Adaptive EPA Crowd Engine
                  </span>
                  <p className="text-xs text-gray-400">
                    Synthesizes pink-noise resonant crowd reactions based on play momentum.
                  </p>
                </div>
              </div>
              <button
                onClick={handleToggleCrowd}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  config.crowdEnabled ? "bg-amber-600" : "bg-gray-800"
                }`}
                role="switch"
                aria-checked={config.crowdEnabled}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    config.crowdEnabled ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            {/* Crowd Audition Buttons */}
            <div className="pt-2 border-t border-white/5">
              <span className="text-[11px] font-mono text-gray-400 uppercase tracking-wider block mb-2">
                Audition Crowd Dynamics:
              </span>
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() =>
                    runAudition("Explosive Roar (+3.5 EPA)", () => soundEffects.updateCrowdIntensity(3.5, 0.8))
                  }
                  className="px-2.5 py-1.5 rounded-lg text-xs font-mono bg-amber-950/60 hover:bg-amber-900/60 border border-amber-500/30 text-amber-200 transition-colors flex items-center justify-center gap-1.5"
                >
                  <Play className="w-3 h-3" />
                  Roar (+3.5 EPA)
                </button>
                <button
                  onClick={() =>
                    runAudition("Turnover Groan (-2.5 EPA)", () => soundEffects.updateCrowdIntensity(-2.5, 0.2))
                  }
                  className="px-2.5 py-1.5 rounded-lg text-xs font-mono bg-amber-950/60 hover:bg-amber-900/60 border border-amber-500/30 text-amber-200 transition-colors flex items-center justify-center gap-1.5"
                >
                  <Play className="w-3 h-3" />
                  Groan (-2.5 EPA)
                </button>
              </div>
            </div>
          </div>

          {/* Sound Effects & Cadence Section */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <div>
                  <span className="text-sm font-semibold uppercase tracking-wide">
                    Sound Effects & Cadence
                  </span>
                  <p className="text-xs text-gray-400">
                    Quarterback voice cadences ("Hut!"), referee whistles, and horns.
                  </p>
                </div>
              </div>
              <button
                onClick={handleToggleSfx}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  config.sfxEnabled ? "bg-purple-600" : "bg-gray-800"
                }`}
                role="switch"
                aria-checked={config.sfxEnabled}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    config.sfxEnabled ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            {/* SFX Audition Buttons */}
            <div className="pt-2 border-t border-white/5">
              <span className="text-[11px] font-mono text-gray-400 uppercase tracking-wider block mb-2">
                Audition Synthesizers:
              </span>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => runAudition("Cadence 'Hut'", () => soundEffects.playCadence("hut"))}
                  className="px-2 py-1.5 rounded-lg text-xs font-mono bg-purple-950/60 hover:bg-purple-900/60 border border-purple-500/30 text-purple-200 transition-colors flex items-center justify-center gap-1"
                >
                  <Play className="w-3 h-3" />
                  Cadence "Hut"
                </button>
                <button
                  onClick={() => runAudition("Ref Whistle", () => soundEffects.playSpatialWhistle(60))}
                  className="px-2 py-1.5 rounded-lg text-xs font-mono bg-purple-950/60 hover:bg-purple-900/60 border border-purple-500/30 text-purple-200 transition-colors flex items-center justify-center gap-1"
                >
                  <Play className="w-3 h-3" />
                  Ref Whistle
                </button>
                <button
                  onClick={() => runAudition("Stadium Horn", () => soundEffects.playStadiumHorn())}
                  className="px-2 py-1.5 rounded-lg text-xs font-mono bg-purple-950/60 hover:bg-purple-900/60 border border-purple-500/30 text-purple-200 transition-colors flex items-center justify-center gap-1"
                >
                  <Play className="w-3 h-3" />
                  Stadium Horn
                </button>
              </div>
            </div>
          </div>

          {/* Last Audition Feedback Pill */}
          {lastAuditioned && (
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-mono animate-fadeIn">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Auditioning: {lastAuditioned} (DSP Triggered)</span>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-white/10 bg-white/5">
          <span className="text-[11px] font-mono text-gray-500">
            Real-Time Web Audio Context • Dynamic Limiter Active
          </span>
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl text-xs font-mono font-bold uppercase tracking-wider bg-emerald-600 hover:bg-emerald-500 text-black transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
