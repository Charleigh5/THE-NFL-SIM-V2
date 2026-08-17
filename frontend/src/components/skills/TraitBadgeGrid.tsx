import React, { useState } from "react";
import { motion } from "framer-motion";
import { Award, Star, Flame } from "lucide-react";
import type { Trait } from "../../types/trait";

interface TraitBadgeGridProps {
  unlockedTraits: string[];
  allTraits?: Trait[];
  onTraitClick?: (traitName: string) => void;
}

interface TraitDisplayItem {
  key: string;
  name: string;
  tier: "LEGENDARY" | "GOLD" | "SILVER" | "BRONZE" | "COMMON";
  category: "QB" | "RB" | "WR/TE" | "OL" | "DL" | "LB" | "DB" | "ST" | "GENERAL" | "LEGENDARY";
  description: string;
  effects: string;
}

export const TraitBadgeGrid: React.FC<TraitBadgeGridProps> = ({
  unlockedTraits,
  onTraitClick,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");
  const [hoveredTrait, setHoveredTrait] = useState<TraitDisplayItem | null>(null);

  // 25+ Trait Catalog from trait_service.py and master dossier
  const catalog: TraitDisplayItem[] = [
    // Legendary
    {
      key: "ragknow",
      name: "Ragknow",
      tier: "LEGENDARY",
      category: "LEGENDARY",
      description: "Ignore injury severity 1-7 penalties entirely. Immune to attribute degradation.",
      effects: "Zero penalty playing through injury • 10% faster recovery • Max cap: 3 players",
    },
    {
      key: "rocket_arm",
      name: "Rocket Arm",
      tier: "LEGENDARY",
      category: "LEGENDARY",
      description: "Elite velocity arm that fits passes into impossible tight windows.",
      effects: "+8 Throw Power • +5 Deep Accuracy • +20% Off-Platform Velocity",
    },
    {
      key: "elite_speed",
      name: "Elite Speed",
      tier: "LEGENDARY",
      category: "LEGENDARY",
      description: "Game-breaking open field velocity.",
      effects: "+3 Speed • +15% Breakaway TD Chance • +20% Closing Speed",
    },
    {
      key: "generational",
      name: "Generational Talent",
      tier: "LEGENDARY",
      category: "LEGENDARY",
      description: "Once-in-a-decade prospect with transcendent development ceiling.",
      effects: "+3 All Ratings • +25% XP Gain • +15% 4th Quarter Clutch",
    },

    // QB
    {
      key: "field_general",
      name: "Field General",
      tier: "GOLD",
      category: "QB",
      description: "Master coordinator who aligns the offense and minimizes mistakes.",
      effects: "+5 Team Awareness • -15% False Starts • +20% Audible Success",
    },
    {
      key: "gunslinger",
      name: "Gunslinger",
      tier: "GOLD",
      category: "QB",
      description: "Aggressive passer who releases fast into tight windows.",
      effects: "+5 Throw Power • -10% Release Time • +5% Interception Risk",
    },
    {
      key: "escape_artist",
      name: "Escape Artist",
      tier: "GOLD",
      category: "QB",
      description: "Elusive scrambler who slips out of collapsing pockets.",
      effects: "+10 Scramble Speed • +10 Agility • +15% Sack Escape Chance",
    },

    // RB
    {
      key: "bruiser",
      name: "Bruiser",
      tier: "GOLD",
      category: "RB",
      description: "Punishing runner who initiates contact and falls forward.",
      effects: "+10 Trucking • +10 Stiff Arm • +25% Fall Forward Chance",
    },
    {
      key: "chip_block_specialist",
      name: "Chip Block Specialist",
      tier: "SILVER",
      category: "RB",
      description: "Expert pass-protecting back who chips edge rushers before releasing.",
      effects: "+40% Chip Block Success • +10 Pass Pro • 15% Rusher Deceleration",
    },
    {
      key: "satellite",
      name: "Satellite Back",
      tier: "SILVER",
      category: "RB",
      description: "Dual-threat back who isolates linebackers in space.",
      effects: "+10 Route Running • +5 Catching • +15% Mismatch Bonus vs LB",
    },

    // WR/TE
    {
      key: "possession_receiver",
      name: "Possession Receiver",
      tier: "GOLD",
      category: "WR/TE",
      description: "Sure-handed target who converts critical 3rd and 4th downs in traffic.",
      effects: "+15 Catch in Traffic • -30% Drop Chance • -25% Fumbles After Catch",
    },
    {
      key: "deep_threat",
      name: "Deep Threat",
      tier: "GOLD",
      category: "WR/TE",
      description: "Field stretcher who stacks cornerbacks on go routes.",
      effects: "+5 Deep Speed • +10 Ball Tracking • +10% Go-Route Separation",
    },
    {
      key: "route_technician",
      name: "Route Technician",
      tier: "GOLD",
      category: "WR/TE",
      description: "Flawless stem breaks and footwork creating immediate separation.",
      effects: "+10 Route Running • +15% Cut Separation • +5 Release vs Press",
    },
    {
      key: "yac_monster",
      name: "YAC Monster",
      tier: "SILVER",
      category: "WR/TE",
      description: "Dangerous after the catch with open-field tackle breaking.",
      effects: "+10 Break Tackle • +10 Elusiveness • +5 Juke Move",
    },
    {
      key: "red_zone_threat",
      name: "Red Zone Threat",
      tier: "GOLD",
      category: "WR/TE",
      description: "High-point jump-ball specialist inside the 20-yard line.",
      effects: "+10 Red Zone Catching • +10 Contested Catch • +10 Endzone Awareness",
    },

    // OL
    {
      key: "anchor",
      name: "Anchor",
      tier: "GOLD",
      category: "OL",
      description: "Immovable pass protector who sinks hips against power rushers.",
      effects: "+10 Strength Blocking • +10 Balance • 50% Pancake Resistance",
    },
    {
      key: "pull_specialist",
      name: "Pull Specialist",
      tier: "SILVER",
      category: "OL",
      description: "Athletic guard/center who leads through outside run alleys.",
      effects: "+10 Pull Speed • +10 Space Blocking • +5 Pull Awareness",
    },

    // DL
    {
      key: "edge_threat",
      name: "Edge Threat",
      tier: "GOLD",
      category: "DL",
      description: "Dominant pass rusher with explosive get-off around the corner.",
      effects: "+10 Acceleration • +5 Finesse Moves • +15% Pressure Generation",
    },
    {
      key: "run_stuffer",
      name: "Run Stuffer",
      tier: "GOLD",
      category: "DL",
      description: "Two-gapping defensive tackle who collapses interior rush lanes.",
      effects: "+10 Block Shedding vs Run • +5 Anchor • +5 Run Tackling",
    },

    // LB
    {
      key: "green_dot",
      name: "Green Dot (Defensive Captain)",
      tier: "GOLD",
      category: "LB",
      description: "Communicates defensive alignments and eliminates blown assignments.",
      effects: "+5 Defense-wide Play Rec • -20% Blown Coverages • +15% Blitz Timing",
    },
    {
      key: "coverage_linebacker",
      name: "Coverage Linebacker",
      tier: "GOLD",
      category: "LB",
      description: "Fluid underneath dropper who mirrors slot receivers and tight ends.",
      effects: "+10 Zone Coverage • +5 Man Coverage • -10% Break Latency",
    },
    {
      key: "enforcer",
      name: "Enforcer",
      tier: "SILVER",
      category: "LB",
      description: "Intimidating tackler who forces fumbles on heavy impact collisions.",
      effects: "+10 Hit Power • +15% Forced Fumble • +20% Fatigue Damage",
    },

    // DB
    {
      key: "pick_artist",
      name: "Pick Artist",
      tier: "GOLD",
      category: "DB",
      description: "Ball-hawk defender with elite hands on intercepted passes.",
      effects: "1.5x Interception Rate • +30% Catch Radius • +15 Ball Tracking",
    },
    {
      key: "shutdown_corner",
      name: "Shutdown Corner",
      tier: "GOLD",
      category: "DB",
      description: "Isolates WR1 in press-man coverage throughout the game.",
      effects: "+10 Man Coverage • +10 Press • -20% Receiver Separation",
    },
    {
      key: "zone_hawk",
      name: "Zone Hawk",
      tier: "GOLD",
      category: "DB",
      description: "Instinctive deep safety reading quarterback eyes.",
      effects: "+10 Zone Coverage • +15% Reaction Speed • +10% Zone INT",
    },

    // ST & General
    {
      key: "clutch_kicker",
      name: "Clutch Kicker",
      tier: "SILVER",
      category: "ST",
      description: "Ice in veins on 4th quarter and overtime game-winning field goals.",
      effects: "+15 Clutch Accuracy • 100% 'Ice the Kicker' Immunity • +5 Power",
    },
    {
      key: "iron_man",
      name: "Iron Man",
      tier: "SILVER",
      category: "GENERAL",
      description: "Exceptional durability through high snap counts.",
      effects: "+20% Fatigue Recovery • +15% Injury Resistance • -10% Stamina Drain",
    },
  ];

  const categories = ["ALL", "LEGENDARY", "QB", "RB", "WR/TE", "OL", "DL", "LB", "DB", "ST", "GENERAL"];

  const filtered = selectedCategory === "ALL"
    ? catalog
    : catalog.filter((t) => t.category === selectedCategory);

  const getTierBadgeStyle = (tier: TraitDisplayItem["tier"]) => {
    switch (tier) {
      case "LEGENDARY":
        return "bg-gradient-to-r from-red-600/30 via-purple-600/30 to-amber-500/30 border-amber-400 text-amber-300 shadow-[0_0_15px_rgba(251,191,36,0.3)]";
      case "GOLD":
        return "bg-amber-950/40 border-amber-500/80 text-amber-300 shadow-[0_0_10px_rgba(245,158,11,0.2)]";
      case "SILVER":
        return "bg-slate-900 border-slate-400 text-slate-200";
      case "BRONZE":
        return "bg-amber-950/20 border-amber-800 text-amber-600";
      default:
        return "bg-slate-900 border-slate-700 text-slate-400";
    }
  };

  return (
    <div className="w-full bg-slate-950/90 border border-slate-800/90 rounded-2xl p-6 shadow-2xl backdrop-blur-xl font-sans">
      {/* Header & Filter Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800 mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-wide uppercase flex items-center gap-2">
              Trait Showcase & Badges
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">
                25+ TRAIT CATALOG
              </span>
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              Passive Modifiers • Situational Matchup Boosts • Legendary Caps
            </p>
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 max-w-full">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold tracking-wider uppercase transition-all whitespace-nowrap ${
                selectedCategory === cat
                  ? "bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-950"
                  : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Trait Badge Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3.5">
        {filtered.map((item) => {
          const isUnlocked = unlockedTraits.includes(item.key) || unlockedTraits.includes(item.name);

          return (
            <motion.div
              key={item.key}
              onMouseEnter={() => setHoveredTrait(item)}
              onMouseLeave={() => setHoveredTrait(null)}
              onClick={() => onTraitClick && onTraitClick(item.name)}
              whileHover={{ scale: 1.02 }}
              className={`relative p-3.5 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                isUnlocked
                  ? getTierBadgeStyle(item.tier)
                  : "bg-slate-900/40 border-slate-800/80 opacity-60 hover:opacity-100 hover:border-slate-700"
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span
                    className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded uppercase tracking-wider ${
                      item.tier === "LEGENDARY"
                        ? "bg-amber-900/80 text-amber-200 border border-amber-600"
                        : item.tier === "GOLD"
                        ? "bg-amber-950 text-amber-300 border border-amber-800"
                        : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    {item.tier}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">
                    {item.category}
                  </span>
                </div>

                <h4 className="font-bold text-sm text-slate-100 flex items-center gap-1.5">
                  {item.tier === "LEGENDARY" && <Flame className="w-3.5 h-3.5 text-amber-400" />}
                  {item.tier === "GOLD" && <Star className="w-3.5 h-3.5 text-amber-400" />}
                  {item.name}
                </h4>

                <p className="text-[11px] text-slate-300 line-clamp-2 mt-1 leading-snug">
                  {item.description}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] font-mono">
                <span className={isUnlocked ? "text-emerald-400 font-bold" : "text-slate-500"}>
                  {isUnlocked ? "ACTIVE BADGE" : "LOCKED"}
                </span>
                <span className="text-slate-400 truncate max-w-[120px]">{item.effects.split("•")[0]}</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Hovered Trait Deep Breakdown Tooltip Footer */}
      {hoveredTrait && (
        <motion.div
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 rounded-xl bg-slate-900/90 border border-slate-700 text-xs font-sans flex flex-wrap items-center justify-between gap-4"
        >
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-white text-sm">{hoveredTrait.name}</span>
              <span className="px-2 py-0.5 rounded bg-amber-950 text-amber-300 font-mono text-[10px] border border-amber-800">
                {hoveredTrait.tier} TIER
              </span>
            </div>
            <p className="text-slate-300 mt-0.5">{hoveredTrait.description}</p>
          </div>
          <div className="bg-slate-950 px-3 py-2 rounded-lg border border-slate-800 text-amber-300 font-mono text-[11px]">
            <strong>Simulation Impact:</strong> {hoveredTrait.effects}
          </div>
        </motion.div>
      )}
    </div>
  );
};
