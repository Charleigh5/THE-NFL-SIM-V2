import React, { useState, useEffect } from "react";
import { useLoaderData, useParams, Link } from "react-router-dom";
import { SkillTreeCanvas } from "../components/skills/SkillTreeCanvas";
import { SkillsOverlay } from "../components/skills/SkillsOverlay";
import { AbilityUnlockTree } from "../components/skills/AbilityUnlockTree";
import { TraitBadgeGrid } from "../components/skills/TraitBadgeGrid";
import { TraitManager } from "../components/dev/TraitManager";
import { ArchetypeBadge } from "../components/player/ArchetypeBadge";
import { SKILL_TREE_LAYOUTS } from "../config/SkillTreeConfig";
import type { Trait as TraitType } from "../types/trait";
import type { PlayerAbilityStatus } from "../types/ability";
import { traitsApi } from "../services/traits";
import { abilitiesApi } from "../services/abilitiesApi";
import type { Player } from "../services/api";
import { Sparkles, ChevronLeft, User, Flame } from "lucide-react";

interface LoaderData {
  player?: Player;
  traits?: TraitType[];
}

export const SkillsPage: React.FC = () => {
  const data = useLoaderData() as LoaderData | null;
  const { playerId } = useParams();

  const [activeTab, setActiveTab] = useState<"3D_TREE" | "ABILITIES" | "TRAITS">("3D_TREE");
  const [selectedTraitId, setSelectedTraitId] = useState<string | null>(null);

  // Player Progression State
  const player = data?.player || {
    id: playerId ? parseInt(playerId) : 1,
    first_name: "Joe",
    last_name: "Burrow",
    position: "QB",
    jersey_number: 9,
    overall_rating: 93,
    age: 27,
    experience: 5,
    team_id: 1,
    awareness: 94,
  };

  const [playerXp, setPlayerXp] = useState<number>(7500);
  const playerLevel = 11;

  // Unlocked traits
  const [unlockedTraits, setUnlockedTraits] = useState<string[]>([
    "field_general",
    "gunslinger",
    "possession_receiver",
    "ragknow",
  ]);

  // Abilities Status State
  const [abilityStatuses, setAbilityStatuses] = useState<Record<string, PlayerAbilityStatus>>({
    pre_snap_diagnostician: {
      key: "pre_snap_diagnostician",
      name: "Pre-Snap Diagnostician",
      description: "Diagnose shell disguises before the snap.",
      status: "AVAILABLE",
      level_required: 10,
      xp_cost: 5000,
      reason: "Ready for unlock",
      effects: { awareness_boost: 15 },
    },
    audible_master: {
      key: "audible_master",
      name: "Audible Master",
      description: "Lightning audible execution.",
      status: "UNLOCKED",
      level_required: 8,
      xp_cost: 3000,
      reason: "Unlocked",
      effects: { audible_time_reduction: 6 },
    },
  });

  // Fetch abilities status on mount
  useEffect(() => {
    if (player?.id) {
      abilitiesApi
        .getPlayerAbilityStatus(player.id)
        .then((res) => {
          if (res && Object.keys(res).length > 0) {
            setAbilityStatuses(res);
          }
        })
        .catch(() => console.log("Using default ability statuses"));
    }
  }, [player?.id]);

  const handleAbilityUnlock = (abilityKey: string, remainingXp?: number) => {
    setAbilityStatuses((prev) => ({
      ...prev,
      [abilityKey]: {
        ...(prev[abilityKey] || {
          key: abilityKey,
          name: abilityKey,
          description: "",
          level_required: 10,
          xp_cost: 4000,
          reason: "Unlocked",
          effects: {},
        }),
        status: "UNLOCKED",
      },
    }));

    if (remainingXp !== undefined) {
      setPlayerXp(remainingXp);
    } else {
      setPlayerXp((prev) => Math.max(0, prev - 4000));
    }
  };

  const handleNodeClick = (traitId: string) => {
    setSelectedTraitId(traitId);
  };

  const handleUnlockOrEquip = async (traitId: string) => {
    if (!unlockedTraits.includes(traitId)) {
      setUnlockedTraits((prev) => [...prev, traitId]);
      try {
        if (player.id) {
          await traitsApi.unlockTrait(player.id, traitId);
        }
      } catch (err) {
        console.warn("Trait unlock backend sync error", err);
      }
    }
  };

  const position = player.position || "QB";
  const layoutKey = SKILL_TREE_LAYOUTS[position] ? position : "QB";
  const layout = SKILL_TREE_LAYOUTS[layoutKey];

  return (
    <div className="w-full h-screen min-h-screen overflow-y-auto bg-slate-950 text-slate-100 p-6 md:p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header Bar */}
        <header className="flex flex-wrap justify-between items-end gap-4 pb-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <Link
              to="/season"
              className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
            </Link>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-400">
                  <Sparkles className="w-5 h-5" />
                </div>
                <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-white">
                  RPG Skill Tree & Ability Hub
                </h1>
              </div>
              <p className="text-xs md:text-sm text-purple-400/90 font-mono">
                Active Abilities • Tiered Trait Badges • Archetype Evolutions
              </p>
            </div>
          </div>

          {/* Player Info & Archetype */}
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-3 bg-slate-900/80 border border-slate-800 px-4 py-2.5 rounded-xl">
              <User className="w-5 h-5 text-purple-400" />
              <div>
                <div className="text-sm font-bold text-white">
                  {player.first_name} {player.last_name}
                </div>
                <div className="text-xs text-slate-400 font-mono">
                  {player.position} • {player.overall_rating} OVR • Level {playerLevel}
                </div>
              </div>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 px-4 py-2 rounded-xl text-right">
              <div className="text-xs text-slate-400 font-mono uppercase">XP Balance</div>
              <div className="text-lg font-bold font-mono text-purple-300">
                {playerXp.toLocaleString()} XP
              </div>
            </div>
          </div>
        </header>

        {/* Archetype Showcase Strip */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-1 bg-slate-900/60 border border-slate-800 p-4 rounded-2xl flex flex-col justify-center items-center">
            <ArchetypeBadge archetype="FIELD_GENERAL" size="lg" showTooltip={true} />
          </div>

          <div className="md:col-span-2 bg-gradient-to-r from-purple-950/40 via-slate-900/80 to-indigo-950/40 border border-purple-500/20 p-5 rounded-2xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono uppercase tracking-wider text-purple-300 flex items-center gap-1.5 font-bold">
                  <Flame className="w-4 h-4 text-purple-400" /> Archetype Combat Impact
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">
                  TIER: PRIMARY
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed mb-3">
                <strong>The Field General:</strong> +5 Awareness, +8 Play Recognition, +10
                Leadership. +20% 3rd-down pass conversion efficiency. Pre-snap coverage audible
                unlocked.
              </p>
            </div>
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 pt-2 border-t border-slate-800">
              <span>
                Career Seasons: <strong>5/3 (Eligible for Evolution)</strong>
              </span>
              <span className="text-emerald-400 font-bold">Evolution Available</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
          <button
            onClick={() => setActiveTab("ABILITIES")}
            className={`px-5 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
              activeTab === "ABILITIES"
                ? "bg-purple-600 text-white shadow-lg shadow-purple-950/50"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            RPG Abilities Tree (7)
          </button>
          <button
            onClick={() => setActiveTab("TRAITS")}
            className={`px-5 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
              activeTab === "TRAITS"
                ? "bg-amber-500 text-slate-950 shadow-lg shadow-amber-950/50"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            Trait Badges & Rarity (25+)
          </button>
          <button
            onClick={() => setActiveTab("3D_TREE")}
            className={`px-5 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${
              activeTab === "3D_TREE"
                ? "bg-cyan-600 text-white shadow-lg shadow-cyan-950/50"
                : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
            }`}
          >
            3D Constellation Visualizer
          </button>
        </div>

        {/* Tab Contents */}
        {activeTab === "ABILITIES" && (
          <AbilityUnlockTree
            playerId={player.id}
            playerLevel={playerLevel}
            playerXp={playerXp}
            playerPosition={player.position}
            abilityStatuses={abilityStatuses}
            onUnlockSuccess={handleAbilityUnlock}
          />
        )}

        {activeTab === "TRAITS" && (
          <div className="space-y-8">
            <TraitBadgeGrid unlockedTraits={unlockedTraits} onTraitClick={handleUnlockOrEquip} />
            <div className="pt-6 border-t border-slate-800">
              <TraitManager
                playerId={player.id}
                playerName={`${player.first_name} ${player.last_name}`}
              />
            </div>
          </div>
        )}

        {activeTab === "3D_TREE" && (
          <div className="w-full h-[650px] relative rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 shadow-2xl">
            <SkillTreeCanvas
              layout={layout}
              unlockedTraits={unlockedTraits}
              equippedTraits={unlockedTraits}
              onNodeClick={handleNodeClick}
            />

            <SkillsOverlay
              selectedTraitId={selectedTraitId}
              selectedTraitDetails={
                selectedTraitId
                  ? ({
                      id: 0,
                      name: selectedTraitId,
                      description: "Active NFL SIM Trait Modifier",
                      effect_type: "PASSIVE",
                      effect_value: 10,
                      tier: "GOLD",
                    } as TraitType)
                  : null
              }
              playerPoints={3}
              onCloseDetail={() => setSelectedTraitId(null)}
              onEquip={handleUnlockOrEquip}
            />
          </div>
        )}
      </div>
    </div>
  );
};
