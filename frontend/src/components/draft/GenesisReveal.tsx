import { useState } from "react";
import { createPortal } from "react-dom";
import { Lock, Activity, AlertTriangle } from "lucide-react";
import type { CombineResult } from "../../types/combine";
import { PlayerAvatar } from "../ui/PlayerAvatar";

interface GenesisRevealProps {
  prospectName: string;
  data: CombineResult;
  onClose: () => void;
  onReveal: () => void;
  isRevealed: boolean;
  playerId?: number;
  position?: string;
}

export const GenesisReveal = ({
  prospectName,
  data,
  onClose,
  onReveal,
  isRevealed,
  playerId,
  position = "ATH",
}: GenesisRevealProps) => {
  const [decrypting, setDecrypting] = useState(false);

  const handleReveal = () => {
    setDecrypting(true);
    setTimeout(async () => {
      try {
        await onReveal();
      } finally {
        setDecrypting(false);
      }
    }, 500); // 500ms decryption animation
  };

  if (typeof document === "undefined") return null;

  return createPortal(
    <div
      className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
      style={{ zIndex: 99999 }}
      data-testid="genesis-modal"
    >
      <div
        className="bg-zinc-900 border border-white/20 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl relative"
        style={{ zIndex: 100000 }}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-zinc-900 to-zinc-800 p-6 border-b border-white/10 text-center relative flex flex-col items-center">
          {playerId && (
            <div className="mb-2">
              <PlayerAvatar
                playerId={playerId}
                teamAbbr="DRAFT"
                pose="headshot"
                size="md"
                position={position}
                playerName={prospectName}
                className="w-14 h-14 rounded-xl border border-cyan-400/40 shadow-lg"
                primaryColor="#22d3ee"
              />
            </div>
          )}
          <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 tracking-tight">
            GENESIS <span className="text-white font-light">INSIGHTS</span>
          </h2>
          <p className="text-gray-400 text-sm mt-1">{prospectName}</p>
          <button
            onClick={onClose}
            data-testid="close-genesis-modal"
            className="absolute top-4 right-4 text-gray-500 hover:text-white p-2 z-20 cursor-pointer"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-8 flex flex-col items-center min-h-[400px] justify-center text-center gap-6">
          {!isRevealed && !decrypting && (
            <>
              <div className="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mb-2 shadow-[0_0_15px_rgba(34,211,238,0.2)]">
                <Lock className="w-10 h-10 text-cyan-400" />
              </div>
              <div className="space-y-4">
                <p className="text-white font-medium text-lg">Encrypted Biometric Data</p>
                <div className="text-gray-400 text-xs text-left bg-black/30 p-4 rounded-lg font-mono leading-relaxed max-w-[300px] mx-auto border border-white/5">
                  <p>• S2 Cognition & Processing Speed</p>
                  <p>• True Physical Measurements</p>
                  <p>• Muscle Fiber Composition</p>
                  <p>• Detailed Medical Screening</p>
                </div>
              </div>
              <button
                onClick={handleReveal}
                className="mt-4 px-10 py-3 bg-cyan-500 hover:bg-cyan-400 text-black font-bold rounded-full hover:scale-105 transition-all shadow-[0_0_20px_rgba(34,211,238,0.4)] flex items-center gap-2"
              >
                <Activity className="w-4 h-4" /> DECRYPT DATA
              </button>
            </>
          )}

          {decrypting && (
            <div className="flex flex-col items-center gap-6">
              <div className="relative">
                <div className="w-16 h-16 border-4 border-cyan-500/30 border-t-cyan-400 rounded-full animate-spin" />
                <div className="w-16 h-16 border-4 border-purple-500/30 border-b-purple-400 rounded-full animate-spin absolute inset-0 animation-delay-150" />
              </div>
              <div className="space-y-1">
                <p className="text-cyan-400 font-mono text-sm animate-pulse tracking-widest">
                  DECRYPTING SECURE FILES...
                </p>
                <p className="text-gray-500 text-[10px] font-mono">ACCESSING MEDICAL DB CL-4</p>
              </div>
            </div>
          )}

          {isRevealed && (
            <div className="w-full animate-in fade-in zoom-in duration-500 space-y-6">
              {/* Primary Stats Grid */}
              <div className="grid grid-cols-3 gap-3 w-full">
                {/* S2 Score */}
                <div className="bg-gradient-to-b from-white/10 to-white/5 p-3 rounded-xl border border-white/10 flex flex-col items-center relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-8 h-8 bg-purple-500/20 blur-xl" />
                  <span className="text-[10px] font-bold tracking-wider text-purple-300 mb-1">
                    S2 SCORE
                  </span>
                  <span className="text-3xl font-bold text-white">
                    {data.s2_cognition_score ?? "N/A"}
                  </span>
                </div>

                {/* Agility Score */}
                <div className="bg-gradient-to-b from-white/10 to-white/5 p-3 rounded-xl border border-white/10 flex flex-col items-center relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-8 h-8 bg-cyan-500/20 blur-xl" />
                  <span className="text-[10px] font-bold tracking-wider text-cyan-300 mb-1">
                    AGILITY
                  </span>
                  <span className="text-3xl font-bold text-white">
                    {data.position_agility_score ?? "--"}
                  </span>
                </div>

                {/* GPS Max */}
                <div className="bg-gradient-to-b from-white/10 to-white/5 p-3 rounded-xl border border-white/10 flex flex-col items-center relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-8 h-8 bg-orange-500/20 blur-xl" />
                  <span className="text-[10px] font-bold tracking-wider text-orange-300 mb-1">
                    GPS MAX
                  </span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-3xl font-bold text-white">
                      {data.gps_speed_max?.toFixed(1) ?? "--"}
                    </span>
                    <span className="text-[10px] text-gray-400">MPH</span>
                  </div>
                </div>
              </div>

              {/* Physical Traits (if available in props, assuming we add them to types later or pass them in details,
                  for now we render placeholders if missing or just what we have)
                  NOTE: data is CombineResult which we just updated.
                  However, standard CombineResult might not have arm_length/wingspan/hand_size unless we add them to interface.
                  We only added power_clean, gps, agility, s2, medical to CombineResult.
                  Ideally these should be in CombineResult too. I'll add them to interface implicitly here or use any.
                  */}
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-black/20 rounded-lg p-3 border border-white/5">
                  <h4 className="text-gray-400 mb-2 font-bold uppercase">Biometrics</h4>
                  <div className="space-y-1">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Fast Twitch</span>
                      <span className="text-white">
                        {data.fast_twitch_percentage ? `${data.fast_twitch_percentage}%` : "--"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Body Fat</span>
                      <span className="text-white">
                        {data.body_fat_percentage ? `${data.body_fat_percentage}%` : "--"}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="bg-black/20 rounded-lg p-3 border border-white/5">
                  <h4 className="text-gray-400 mb-2 font-bold uppercase">Measurements</h4>
                  <div className="space-y-1">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Hands</span>
                      <span className="text-white">
                        {data.hand_size ? `${data.hand_size}"` : "--"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Wingspan</span>
                      <span className="text-white">
                        {data.wingspan ? `${data.wingspan}"` : "--"}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Medicals */}
              <div
                className={`w-full border rounded-xl p-4 text-left transition-colors ${
                  data.medical_flags && data.medical_flags.length > 0
                    ? "bg-red-500/10 border-red-500/30"
                    : "bg-emerald-500/10 border-emerald-500/30"
                }`}
              >
                <div
                  className={`flex items-center gap-2 mb-3 text-xs font-bold tracking-wider ${
                    data.medical_flags && data.medical_flags.length > 0
                      ? "text-red-400"
                      : "text-emerald-400"
                  }`}
                >
                  <AlertTriangle className="w-4 h-4" />
                  <span>MEDICAL FLAGS</span>
                </div>
                {data.medical_flags && data.medical_flags.length > 0 ? (
                  <ul className="text-sm text-gray-300 space-y-2">
                    {data.medical_flags.map((flag, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-red-500 mt-1">•</span>
                        <span>{flag.replace(/_/g, " ")}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-emerald-400 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
                    Clean Bill of Health Verified
                  </p>
                )}
              </div>

              {/* Action Buttons */}
              <button
                type="button"
                onClick={onClose}
                data-testid="close-modal-bottom"
                className="w-full py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-bold tracking-wider uppercase transition-colors"
              >
                Close Insights
              </button>
            </div>
          )}
        </div>
      </div>
    </div>,
    document.body
  );
};
