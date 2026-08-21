import React, { useState } from "react";
import { motion } from "framer-motion";
import { Brain, Lock, CheckCircle2, Zap, Sparkles, Shield, Compass, Target } from "lucide-react";
import type { PlayerAbilityStatus, PreSnapInsightResponse } from "../../types/ability";
import { abilitiesApi } from "../../services/abilitiesApi";

interface AbilityUnlockTreeProps {
  playerId: number;
  playerLevel: number;
  playerXp: number;
  playerPosition: string;
  abilityStatuses: Record<string, PlayerAbilityStatus>;
  onUnlockSuccess: (abilityKey: string, remainingXp?: number) => void;
}

export const AbilityUnlockTree: React.FC<AbilityUnlockTreeProps> = ({
  playerId,
  playerLevel,
  playerXp,
  playerPosition,
  abilityStatuses,
  onUnlockSuccess,
}) => {
  const [selectedAbility, setSelectedAbility] = useState<string | null>("pre_snap_diagnostician");
  const [unlockingKey, setUnlockingKey] = useState<string | null>(null);
  const [insightLoading, setInsightLoading] = useState<boolean>(false);
  const [preSnapInsight, setPreSnapInsight] = useState<PreSnapInsightResponse | null>(null);

  // Complete catalog of 7 RPG Abilities with UI icons & metadata
  const catalog: Record<
    string,
    {
      key: string;
      name: string;
      positions: string[];
      levelReq: number;
      xpCost: number;
      icon: React.ReactNode;
      mechanic: string;
    }
  > = {
    pre_snap_diagnostician: {
      key: "pre_snap_diagnostician",
      name: "Pre-Snap Diagnostician",
      positions: ["QB"],
      levelReq: 10,
      xpCost: 5000,
      icon: <Brain className="w-5 h-5" />,
      mechanic:
        "Unlocks 'The Read' pre-snap coverage insight (90% read accuracy vs disguised shells).",
    },
    audible_master: {
      key: "audible_master",
      name: "Audible Master",
      positions: ["QB"],
      levelReq: 8,
      xpCost: 3000,
      icon: <Zap className="w-5 h-5" />,
      mechanic:
        "Reduces audible latency from 8s to 2s; false-start immunity on blitz check audibles.",
    },
    red_zone_assassin: {
      key: "red_zone_assassin",
      name: "Red Zone Assassin",
      positions: ["QB"],
      levelReq: 12,
      xpCost: 6000,
      icon: <Target className="w-5 h-5" />,
      mechanic: "+10 Red Zone Accuracy, +15% TD conversion chance inside the 20-yard line.",
    },
    vision_master: {
      key: "vision_master",
      name: "Vision Master",
      positions: ["RB"],
      levelReq: 8,
      xpCost: 3500,
      icon: <Compass className="w-5 h-5" />,
      mechanic: "+15 Ball Carrier Vision, highlights optimal cutback lanes before contact.",
    },
    route_tree_genius: {
      key: "route_tree_genius",
      name: "Route Tree Genius",
      positions: ["WR", "TE"],
      levelReq: 10,
      xpCost: 4500,
      icon: <Sparkles className="w-5 h-5" />,
      mechanic: "+10 Route Running, unlocks real-time option-route choice based on coverage.",
    },
    film_junkie: {
      key: "film_junkie",
      name: "Film Junkie",
      positions: ["LB", "S", "CB"],
      levelReq: 8,
      xpCost: 3000,
      icon: <Brain className="w-5 h-5" />,
      mechanic: "+10 Play Recognition, 75% accuracy predicting opponent run vs pass direction.",
    },
    coverage_chameleon: {
      key: "coverage_chameleon",
      name: "Coverage Chameleon",
      positions: ["CB", "S"],
      levelReq: 10,
      xpCost: 5000,
      icon: <Shield className="w-5 h-5" />,
      mechanic: "+8 Man & Zone Coverage, seamless disguise transitions between shells.",
    },
  };

  const handleUnlock = async (key: string) => {
    setUnlockingKey(key);
    try {
      const res = await abilitiesApi.unlockAbility(playerId, key);
      if (res.success) {
        onUnlockSuccess(key, res.remaining_xp);
      }
    } catch {
      // Optimistic unlock fallback in offline/demo mode
      onUnlockSuccess(key, Math.max(0, playerXp - (catalog[key]?.xpCost || 3000)));
    } finally {
      setUnlockingKey(null);
    }
  };

  const handleRunPreSnapSimulation = async () => {
    setInsightLoading(true);
    try {
      const res = await abilitiesApi.getPreSnapInsight({ qb_id: playerId });
      setPreSnapInsight(res);
    } catch {
      // Demo simulation
      const coverages = ["Cover 2 Shell", "Cover 3 Match", "Cover 1 Robber", "Cover 0 Blitz"];
      const randomCov = coverages[Math.floor(Math.random() * coverages.length)];
      setPreSnapInsight({
        has_ability: true,
        predicted_coverage: randomCov,
        confidence: "High",
        key_read: "Safety rotational creep detected. Outside leverage on perimeter receiver.",
        is_correct: true,
      });
    } finally {
      setInsightLoading(false);
    }
  };

  return (
    <div className="w-full bg-slate-950/90 border border-slate-800/90 rounded-2xl p-6 shadow-2xl backdrop-blur-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800 mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide uppercase flex items-center gap-2">
              RPG Ability Tree
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">
                ACTIVE MECHANICS
              </span>
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              Level {playerLevel} • Available Progression XP:{" "}
              <strong className="text-purple-300 font-bold font-mono">
                {playerXp.toLocaleString()} XP
              </strong>
            </p>
          </div>
        </div>
      </div>

      {/* Grid of Abilities */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {Object.values(catalog).map((item) => {
          const statusObj = abilityStatuses[item.key];
          const isUnlocked = statusObj?.status === "UNLOCKED";
          const isEligiblePosition =
            item.positions.includes(playerPosition) || item.positions.includes("ALL");
          const meetsLevel = playerLevel >= item.levelReq;
          const meetsXp = playerXp >= item.xpCost;
          const canUnlock = !isUnlocked && meetsLevel && meetsXp && isEligiblePosition;
          const isSelected = selectedAbility === item.key;

          return (
            <div
              key={item.key}
              onClick={() => setSelectedAbility(item.key)}
              className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? "bg-slate-900 border-purple-500 shadow-lg shadow-purple-950/40"
                  : isUnlocked
                    ? "bg-purple-950/20 border-purple-500/40 hover:border-purple-400"
                    : "bg-slate-900/50 border-slate-800 hover:border-slate-700"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div
                    className={`p-2 rounded-lg ${
                      isUnlocked
                        ? "bg-purple-900/60 text-purple-300 border border-purple-500/50"
                        : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    {item.icon}
                  </div>
                  <div className="flex items-center gap-1">
                    {isUnlocked ? (
                      <span className="flex items-center gap-1 text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800">
                        <CheckCircle2 className="w-3 h-3" /> UNLOCKED
                      </span>
                    ) : meetsLevel ? (
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                        LVL {item.levelReq} READY
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                        <Lock className="w-3 h-3" /> LVL {item.levelReq}
                      </span>
                    )}
                  </div>
                </div>

                <h4 className="font-bold text-sm text-slate-100 mb-1">{item.name}</h4>
                <p className="text-xs text-slate-400 leading-relaxed mb-3">{item.mechanic}</p>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono">
                <span className="text-slate-400">{item.xpCost.toLocaleString()} XP</span>
                {isUnlocked ? (
                  <span className="text-purple-300 font-bold">Active in Play</span>
                ) : (
                  <button
                    disabled={!canUnlock || unlockingKey === item.key}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleUnlock(item.key);
                    }}
                    className={`px-3 py-1 rounded text-xs font-bold uppercase tracking-wider transition-all ${
                      canUnlock
                        ? "bg-purple-600 hover:bg-purple-500 text-white shadow-md shadow-purple-950"
                        : "bg-slate-800 text-slate-500 cursor-not-allowed"
                    }`}
                  >
                    {unlockingKey === item.key ? "Unlocking..." : "Unlock"}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Active Feature Spotlight / Pre-Snap Read Interactive Simulator */}
      {selectedAbility === "pre_snap_diagnostician" && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-5 rounded-xl bg-gradient-to-r from-purple-950/30 via-slate-900 to-indigo-950/30 border border-purple-500/30"
        >
          <div className="flex flex-wrap items-center justify-between gap-4 mb-3">
            <div>
              <h4 className="text-sm font-bold text-purple-300 uppercase tracking-wider flex items-center gap-2">
                <Brain className="w-4 h-4" /> Live "The Read" Simulator (Diagnostician Engine)
              </h4>
              <p className="text-xs text-slate-400">
                Simulate how QB Awareness + Level cuts through the Defensive Coordinator's coverage
                disguise.
              </p>
            </div>
            <button
              onClick={handleRunPreSnapSimulation}
              disabled={insightLoading}
              className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-lg"
            >
              {insightLoading ? "Scanning Shell..." : "Run Pre-Snap Read"}
            </button>
          </div>

          {preSnapInsight && (
            <div className="p-3.5 rounded-lg bg-slate-950/80 border border-purple-500/20 text-xs font-mono space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Predicted Coverage Shell:</span>
                <span className="text-cyan-400 font-bold text-sm">
                  {preSnapInsight.predicted_coverage}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Confidence Metric:</span>
                <span className="text-emerald-400 font-bold">
                  {preSnapInsight.confidence} Confidence
                </span>
              </div>
              <div className="pt-2 border-t border-slate-800 text-purple-300">
                <strong className="text-slate-400">Telemetry Read:</strong> "
                {preSnapInsight.key_read}"
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
};
