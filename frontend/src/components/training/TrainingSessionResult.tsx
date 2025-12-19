import React from "react";
import { motion } from "framer-motion";
import { Check, AlertTriangle, TrendingUp, Activity, BarChart2 } from "lucide-react";
import type { TrainingResult } from "../../types/training";

interface TrainingSessionResultProps {
  result: TrainingResult;
  onClose: () => void;
}

export const TrainingSessionResult: React.FC<TrainingSessionResultProps> = ({
  result,
  onClose,
}) => {
  const isInjury = result.injury_occurred;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
    >
      <div className="w-full max-w-lg bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl overflow-hidden relative">
        {/* Background Effect */}
        <div
          className={`absolute top-0 left-0 w-full h-2 bg-gradient-to-r ${isInjury ? "from-red-500 to-orange-500" : "from-green-400 to-blue-500"}`}
        />

        <div className="p-8">
          {/* Header Icon */}
          <div className="flex justify-center mb-6">
            <div className={`p-4 rounded-full ${isInjury ? "bg-red-500/20" : "bg-green-500/20"}`}>
              {isInjury ? (
                <AlertTriangle className="w-12 h-12 text-red-500" />
              ) : (
                <Check className="w-12 h-12 text-green-500" />
              )}
            </div>
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-white text-center mb-2">
            {isInjury ? "Injury Report" : "Training Complete"}
          </h2>
          <p className="text-gray-400 text-center mb-8">
            {isInjury
              ? "An incident occurred during the session."
              : "Great work! Session completed successfully."}
          </p>

          {/* XP Gains Section */}
          {!isInjury && (
            <div className="bg-gray-800/50 rounded-xl p-6 mb-6 border border-gray-700/50">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <h3 className="text-lg font-semibold text-white">XP Gains</h3>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center group">
                  <span className="text-gray-300 font-medium">{result.target_stat}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500 uppercase tracking-widest group-hover:text-green-400/70 transition-colors">
                      Target
                    </span>
                    <span className="text-xl font-bold text-green-400">+{result.xp_gained} XP</span>
                  </div>
                </div>

                {result.secondary_stats && result.secondary_stats.length > 0 && (
                  <div className="pt-3 border-t border-gray-700/50">
                    <p className="text-xs text-gray-500 mb-2">Secondary Effects</p>
                    {result.secondary_stats.map((stat) => (
                      <div key={stat} className="flex justify-between items-center text-sm py-1">
                        <span className="text-gray-400">{stat}</span>
                        <span className="text-green-500/80 font-mono">
                          +{(result.xp_gained * 0.2).toFixed(0)} XP
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Fatigue & Risk Stats */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="bg-gray-800/30 p-4 rounded-xl border border-gray-700/30">
              <div className="flex items-center gap-2 mb-2 text-gray-400">
                <Activity className="w-4 h-4" />
                <span className="text-xs uppercase tracking-wider">Fatigue</span>
              </div>
              <div className="text-xl font-bold text-white">
                +{result.fatigue_added.toFixed(0)}{" "}
                <span className="text-sm font-normal text-gray-500">%</span>
              </div>
            </div>
            <div className="bg-gray-800/30 p-4 rounded-xl border border-gray-700/30">
              <div className="flex items-center gap-2 mb-2 text-gray-400">
                <BarChart2 className="w-4 h-4" />
                <span className="text-xs uppercase tracking-wider">Weekly Load</span>
              </div>
              <div className="text-xl font-bold text-white">{result.weekly_load}%</div>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={onClose}
            className={`w-full py-3 rounded-xl font-bold transition-all transform hover:scale-[1.02] active:scale-[0.98] ${
              isInjury
                ? "bg-red-600 hover:bg-red-500 text-white shadow-lg shadow-red-900/20"
                : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/20"
            }`}
          >
            {isInjury ? "Acknowledge" : "Continue"}
          </button>
        </div>
      </div>
    </motion.div>
  );
};
