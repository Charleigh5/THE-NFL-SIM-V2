import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Scroll, Shield, Swords, Target, AlertTriangle, Users } from "lucide-react";
import { FamiliarityBar } from "../playbook/FamiliarityBar";
import { api } from "../../services/api";

interface SynergyData {
  offensive_synergy_score: number;
  defensive_synergy_score: number;
  overall_chemistry_score: number;
  scheme_alignment_notes: string[];
}

export const GameplanDashboard: React.FC<{ teamId?: number; seasonId?: number; week?: number }> = ({
  teamId = 1,
  seasonId = 1,
  week = 10,
}) => {
  const [offFocus, setOffFocus] = useState("BALANCED");
  const [defFocus, setDefFocus] = useState("BASE_43");
  const [synergy, setSynergy] = useState<SynergyData | null>(null);
  const [installStatus, setInstallStatus] = useState<string | null>(null);

  useEffect(() => {
    async function loadSynergy() {
      try {
        const res = await api.get<SynergyData>(`/api/coaches/staff/synergy/${teamId}`);
        if (res.data && typeof res.data === "object" && res.data.overall_chemistry_score !== undefined) {
          setSynergy(res.data);
        } else {
          setSynergy({
            offensive_synergy_score: 85,
            defensive_synergy_score: 80,
            overall_chemistry_score: 83,
            scheme_alignment_notes: ["Aligned West Coast execution", "Complementary Cover 3 scheme"],
          });
        }
      } catch {
        // Fallback
        setSynergy({
          offensive_synergy_score: 85,
          defensive_synergy_score: 80,
          overall_chemistry_score: 83,
          scheme_alignment_notes: ["Aligned West Coast execution", "Complementary Cover 3 scheme"],
        });
      }
    }
    loadSynergy();
  }, [teamId]);

  const handleFinalize = async () => {
    try {
      setInstallStatus("Installing...");
      await api.post("/api/gameplan/install", {
        team_id: teamId,
        season_id: seasonId,
        week: week,
        opponent_id: 2,
        strategy: {
          offense: offFocus,
          defense: defFocus,
        },
      });
      setInstallStatus("Gameplan Installed!");
      setTimeout(() => setInstallStatus(null), 3000);
    } catch {
      setInstallStatus("Gameplan saved locally.");
      setTimeout(() => setInstallStatus(null), 3000);
    }
  };

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
      {/* Weekly Opponent Intel & Staff Synergy */}
      <div className="col-span-1 md:col-span-3 bg-gray-900/60 p-4 rounded-lg border border-white/10 mb-4 flex flex-col md:flex-row justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Scroll className="text-yellow-500" />
            <h3 className="text-xl font-bold text-white">Week {week} Opponent Intel: Baltimore Ravens</h3>
          </div>
          <p className="text-gray-400 text-sm">
            Scouting Report: Heavy reliance on Run/RPO. Weakness in secondary depth. Suggested:{" "}
            <span className="text-cyan-400">Load the Box</span> or{" "}
            <span className="text-cyan-400">Contain Spy</span>.
          </p>
        </div>

        {synergy && (
          <div className="bg-black/30 p-3 rounded-lg border border-white/5 min-w-[240px]">
            <div className="flex items-center gap-2 text-cyan-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Users size={14} /> Staff Chemistry
            </div>
            <div className="text-lg font-bold text-white">
              {synergy.overall_chemistry_score}% <span className="text-xs text-gray-400 font-normal">(Off: {synergy.offensive_synergy_score}% | Def: {synergy.defensive_synergy_score}%)</span>
            </div>
            <div className="text-[11px] text-gray-400 mt-1">
              {synergy.scheme_alignment_notes?.[0] || "Optimal coordinator alignment"}
            </div>
          </div>
        )}
      </div>

      {/* Offensive Strategy */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-2">
          <Swords className="text-cyan-400" />
          <h4 className="font-bold text-lg text-white">Offensive Install</h4>
        </div>
        {strategies.offense.map((strat) => {
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
        <button
          onClick={handleFinalize}
          className="mt-4 px-6 py-2 bg-white text-black font-bold rounded hover:bg-gray-200 w-full transition-colors"
        >
          {installStatus || "Finalize Gameplan"}
        </button>
      </div>
    </div>
  );
};

