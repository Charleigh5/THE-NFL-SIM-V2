import React, { useState } from "react";
import { motion } from "framer-motion";
import { Scroll, Shield, Swords, Target, AlertTriangle } from "lucide-react";
import { FamiliarityBar } from "../playbook/FamiliarityBar";

export const GameplanDashboard: React.FC = () => {
  const [offFocus, setOffFocus] = useState("BALANCED");
  const [defFocus, setDefFocus] = useState("BASE_43");

  const strategies = {
    offense: [
      { id: "RUN_HEAVY", name: "Establish The Run", desc: "+5 Run Blocking, -2 Pass Pro" },
      { id: "AIR_RAID", name: "Air Raid", desc: "+5 Pass Acc, -5 Run Blk" },
      { id: "BALANCED", name: "Pro Style Balanced", desc: "No bonuses or penalties" },
      { id: "PA_HEAVY", name: "Play Action Heavy", desc: "+3 PA Eff, +2 Run Blk" },
    ],
    defense: [
      { id: "BLITZ_HEAVY", name: "Blitzburgh", desc: "+5 Pass Rush, -3 Coverage" },
      { id: "COVER_2", name: "Tampa 2", desc: "+5 Zone Cov, -3 Run Def" },
      { id: "BASE_43", name: "Base 4-3", desc: "Balanced front" },
      { id: "MAN_FREE", name: "Man Free", desc: "+4 Man Cov, +2 Blitz" },
    ],
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
      {/* Weekly Opponent Intel */}
      <div className="col-span-1 md:col-span-3 bg-gray-900/60 p-4 rounded-lg border border-white/10 mb-4">
        <div className="flex items-center gap-3 mb-2">
          <Scroll className="text-yellow-500" />
          <h3 className="text-xl font-bold text-white">Week 10 Opponent Intel: Baltimore Ravens</h3>
        </div>
        <p className="text-gray-400 text-sm">
          Scouting Report: Heavy reliance on Run/RPO. Weakness in secondary depth. Suggested:{" "}
          <span className="text-cyan-400">Load the Box</span> or{" "}
          <span className="text-cyan-400">Contain Spy</span>.
        </p>
      </div>

      {/* Offensive Strategy */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-2">
          <Swords className="text-cyan-400" />
          <h4 className="font-bold text-lg text-white">Offensive Install</h4>
        </div>
        {strategies.offense.map((strat) => {
          // Mock familiarity depending on strategy for demo
          // In real app, this would come from backend B-048
          const familiarityScore =
            strat.id === "BALANCED" ? 0.95 : strat.id === "AIR_RAID" ? 0.35 : 0.65;

          return (
            <motion.div
              key={strat.id}
              onClick={() => setOffFocus(strat.id)}
              className={`p-4 rounded-lg border cursor-pointer transition-colors relative overflow-hidden ${
                offFocus === strat.id
                  ? "bg-cyan-900/40 border-cyan-400"
                  : "bg-black/20 border-white/5 hover:border-white/20"
              }`}
              whileHover={{ x: 5 }}
            >
              <div className="font-bold text-white flex justify-between">{strat.name}</div>
              <div className="text-xs text-gray-400 mb-2">{strat.desc}</div>

              <FamiliarityBar score={familiarityScore} showLabel={true} />

              {/* Warning for low familiarity */}
              {offFocus === strat.id && familiarityScore < 0.5 && (
                <div className="mt-2 text-[10px] text-red-300 bg-red-500/10 border border-red-500/30 p-1.5 rounded flex items-center gap-1 animate-in fade-in slide-in-from-top-1">
                  <AlertTriangle className="w-3 h-3" />
                  <span>Critical unfamiliarity penalty active.</span>
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Defensive Strategy */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-2">
          <Shield className="text-red-400" />
          <h4 className="font-bold text-lg text-white">Defensive Install</h4>
        </div>
        {strategies.defense.map((strat) => {
          // Mock familiarity depending on strategy for demo
          // In real app, this would come from backend B-048
          const familiarityScore =
            strat.id === "BASE_43" ? 0.95 : strat.id === "COVER_2" ? 0.45 : 0.75;

          return (
            <motion.div
              key={strat.id}
              onClick={() => setDefFocus(strat.id)}
              className={`p-4 rounded-lg border cursor-pointer transition-colors relative overflow-hidden ${
                defFocus === strat.id
                  ? "bg-red-900/40 border-red-400"
                  : "bg-black/20 border-white/5 hover:border-white/20"
              }`}
              whileHover={{ x: 5 }}
            >
              <div className="font-bold text-white flex justify-between">{strat.name}</div>
              <div className="text-xs text-gray-400 mb-2">{strat.desc}</div>

              <FamiliarityBar score={familiarityScore} showLabel={true} />

              {/* Warning for low familiarity */}
              {defFocus === strat.id && familiarityScore < 0.5 && (
                <div className="mt-2 text-[10px] text-red-300 bg-red-500/10 border border-red-500/30 p-1.5 rounded flex items-center gap-1 animate-in fade-in slide-in-from-top-1">
                  <AlertTriangle className="w-3 h-3" />
                  <span>Inefficient! -25% Execution until learned.</span>
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Summary / Bonus */}
      <div className="p-4 bg-gradient-to-br from-gray-800 to-black rounded-lg border border-white/10 flex flex-col justify-center items-center text-center">
        <Target size={48} className="text-green-500 mb-2" />
        <h4 className="font-bold text-white text-lg">Focus Bonus</h4>
        <div className="text-sm text-gray-400 mt-2">
          Proj. Efficiency: <span className="text-green-400 font-bold">92%</span>
        </div>
        <button className="mt-4 px-6 py-2 bg-white text-black font-bold rounded hover:bg-gray-200 w-full">
          Finalize Gameplan
        </button>
      </div>
    </div>
  );
};
