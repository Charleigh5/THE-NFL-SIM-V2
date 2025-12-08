import { useState } from "react";
import { Lock, Activity, Brain, AlertTriangle } from "lucide-react";
import type { CombineResult } from "../../types/combine";

interface GenesisRevealProps {
  prospectName: string;
  data: CombineResult;
  onClose: () => void;
  onReveal: () => void;
  isRevealed: boolean;
}

export const GenesisReveal = ({
  prospectName,
  data,
  onClose,
  onReveal,
  isRevealed,
}: GenesisRevealProps) => {
  const [decrypting, setDecrypting] = useState(false);

  const handleReveal = () => {
    setDecrypting(true);
    setTimeout(() => {
      setDecrypting(false);
      onReveal();
    }, 1500); // 1.5s decryption animation
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-zinc-900 border border-white/20 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-zinc-900 to-zinc-800 p-6 border-b border-white/10 text-center relative">
          <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 tracking-tight">
            GENESIS <span className="text-white font-light">INSIGHTS</span>
          </h2>
          <p className="text-gray-400 text-sm mt-1">{prospectName}</p>
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-500 hover:text-white"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-8 flex flex-col items-center min-h-[300px] justify-center text-center gap-6">
          {!isRevealed && !decrypting && (
            <>
              <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-2">
                <Lock className="w-8 h-8 text-gray-400" />
              </div>
              <div>
                <p className="text-gray-300 font-medium">Encrypted Biometric Data</p>
                <p className="text-gray-500 text-xs mt-2 max-w-[240px] mx-auto">
                  Contains S2 Cognition scoring, deep medical history, and detailed GPS telemetry.
                </p>
              </div>
              <button
                onClick={handleReveal}
                className="mt-4 px-8 py-3 bg-white text-black font-bold rounded-full hover:bg-cyan-400 hover:scale-105 transition-all shadow-lg"
              >
                DECRYPT DATA (50 SC)
              </button>
            </>
          )}

          {decrypting && (
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" />
              <p className="text-cyan-400 font-mono text-sm animate-pulse">
                DECRYPTING SECURE FILES...
              </p>
            </div>
          )}

          {isRevealed && (
            <div className="w-full animate-in fade-in zoom-in duration-500">
              <div className="grid grid-cols-2 gap-4 w-full mb-6">
                {/* S2 Score */}
                <div className="bg-white/5 p-4 rounded-xl border border-white/10 flex flex-col items-center">
                  <div className="flex items-center gap-2 mb-2 text-cyan-300">
                    <Brain className="w-4 h-4" />
                    <span className="text-xs font-bold tracking-wider">S2 SCORE</span>
                  </div>
                  <span className="text-4xl font-bold text-white">
                    {data.s2_cognition_score ?? "N/A"}
                  </span>
                </div>

                {/* Max Speed */}
                <div className="bg-white/5 p-4 rounded-xl border border-white/10 flex flex-col items-center">
                  <div className="flex items-center gap-2 mb-2 text-orange-300">
                    <Activity className="w-4 h-4" />
                    <span className="text-xs font-bold tracking-wider">GPS MAX</span>
                  </div>
                  <span className="text-4xl font-bold text-white">
                    {data.gps_speed_max?.toFixed(1) ?? "--"}
                  </span>
                  <span className="text-[10px] text-gray-500">MPH</span>
                </div>
              </div>

              {/* Medicals */}
              <div className="w-full bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-left">
                <div className="flex items-center gap-2 mb-3 text-red-400">
                  <AlertTriangle className="w-4 h-4" />
                  <span className="text-xs font-bold tracking-wider">MEDICAL FLAGS</span>
                </div>
                {data.medical_flags && data.medical_flags.length > 0 ? (
                  <ul className="text-sm text-gray-300 space-y-1 list-disc list-inside">
                    {data.medical_flags.map((flag, idx) => (
                      <li key={idx}>{flag}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-emerald-400 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full" />
                    Clean Bill of Health
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
