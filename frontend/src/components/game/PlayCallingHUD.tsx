import React, { useState, useEffect } from "react";
import { apiClient } from "../../services/api";
import { soundEffects } from "../../services/soundEffects";
import {
  Play,
  Shield,
  Zap,
  Target,
  ChevronUp,
  ChevronDown,
  TrendingUp,
  Layers,
  Flame,
  CheckCircle,
} from "lucide-react";

export type PlayCategory = "RUN" | "PASS" | "DEFENSE" | "SPECIAL_TEAMS";

export interface TacticalConcept {
  id: string;
  name: string;
  category: PlayCategory;
  playType: "RUN" | "PASS" | "FIELD_GOAL" | "PUNT" | "SPIKE" | "KNEEL";
  riskReward: "SAFE" | "BALANCED" | "AGGRESSIVE";
  description: string;
  tags: string[];
}

interface PlayCallingHUDProps {
  gameId?: number;
  teamId?: number;
  isOffense?: boolean;
  down?: number;
  distance?: number;
  yardline?: number;
  scoreDiff?: number;
  isCoachMode?: boolean;
  onToggleCoachMode?: (mode: boolean) => void;
  onPlayCallSubmitted?: (playType: string, conceptId: string) => void;
  onOpenFourthDownModal?: () => void;
  selectedIndex?: number | null;
  externalCategory?: PlayCategory | null;
}

const TACTICAL_CONCEPTS: TacticalConcept[] = [
  // RUN CONCEPTS
  {
    id: "inside_zone",
    name: "Inside Zone Split",
    category: "RUN",
    playType: "RUN",
    riskReward: "SAFE",
    description: "Double teams at the point of attack, cutback lane behind pulling tight end.",
    tags: ["A-Gap", "Duo", "High Floor"],
  },
  {
    id: "stretch_run",
    name: "Outside Zone Stretch",
    category: "RUN",
    playType: "RUN",
    riskReward: "BALANCED",
    description: "Edge horizontal stretch forcing pursuit angles, explosive cutback potential.",
    tags: ["B-Gap", "Speed", "Perimeter"],
  },
  {
    id: "power_counter",
    name: "GT Counter / Power",
    category: "RUN",
    playType: "RUN",
    riskReward: "AGGRESSIVE",
    description: "Guard & tackle pulling downhill through opposite C-gap with lead fullback block.",
    tags: ["Heavy", "Gap Scheme", "Physical"],
  },
  // PASS CONCEPTS
  {
    id: "slants",
    name: "Dragon Quick Slants",
    category: "PASS",
    playType: "PASS",
    riskReward: "SAFE",
    description: "3-step drop rhythm strike underneath flat defenders against man or zone blitz.",
    tags: ["Rhythm", "High Comp%", "Blitz Beater"],
  },
  {
    id: "mesh",
    name: "Mesh Crossers",
    category: "PASS",
    playType: "PASS",
    riskReward: "BALANCED",
    description: "Dual shallow crossing routes creating rub traffic with running back wheel valve.",
    tags: ["Man Beater", "YAC", "Chain Mover"],
  },
  {
    id: "flood",
    name: "Sail Flood Concept",
    category: "PASS",
    playType: "PASS",
    riskReward: "BALANCED",
    description: "High-low 3-level stretch attacking Cover 3 sideline zone with deep corner and out.",
    tags: ["Zone Buster", "Intermediate", "Sideline"],
  },
  {
    id: "four_verticals",
    name: "Four Verticals Shot",
    category: "PASS",
    playType: "PASS",
    riskReward: "AGGRESSIVE",
    description: "All four receivers pushing vertical seams to stress single-high safeties deep.",
    tags: ["Deep Shot", "Explosive", "Aggressive"],
  },
  // DEFENSIVE CONCEPTS
  {
    id: "cover_3",
    name: "Cover 3 Sky Zone",
    category: "DEFENSE",
    playType: "PASS",
    riskReward: "SAFE",
    description: "3 deep third defenders with 4 underneath underneath hook/curl zones.",
    tags: ["Base", "Bend Don't Break", "Anti-Deep"],
  },
  {
    id: "cover_2_tampa",
    name: "Tampa 2 Invert",
    category: "DEFENSE",
    playType: "PASS",
    riskReward: "BALANCED",
    description: "Deep middle run-through by MLB with dual half-field safeties bracketing boundaries.",
    tags: ["Intermediate", "Middle Shield", "Zone"],
  },
  {
    id: "cover_1_man",
    name: "Cover 1 Man-Free",
    category: "DEFENSE",
    playType: "PASS",
    riskReward: "BALANCED",
    description: "Lockdown press man coverage across perimeter with single-high centerfield safety.",
    tags: ["Aggressive", "Press", "Tight Window"],
  },
  {
    id: "fire_zone",
    name: "Cross-Dog Fire Blitz",
    category: "DEFENSE",
    playType: "PASS",
    riskReward: "AGGRESSIVE",
    description: "5-man overload rush sending inside linebackers through A/B gaps with 3-under 3-deep.",
    tags: ["Sack Threat", "Pressure", "High Risk"],
  },
  // SPECIAL TEAMS
  {
    id: "field_goal",
    name: "Field Goal Unit",
    category: "SPECIAL_TEAMS",
    playType: "FIELD_GOAL",
    riskReward: "SAFE",
    description: "Standard placekick operation with maximum protection.",
    tags: ["3 Points", "Special Teams"],
  },
  {
    id: "punt_unit",
    name: "Punt Shield Coverage",
    category: "SPECIAL_TEAMS",
    playType: "PUNT",
    riskReward: "SAFE",
    description: "Punt execution aiming to pin returner inside the 20.",
    tags: ["Field Position", "Special Teams"],
  },
];

export const PlayCallingHUD: React.FC<PlayCallingHUDProps> = ({
  gameId = 1,
  teamId = 1,
  isOffense = true,
  down = 1,
  distance = 10,
  yardline = 25,
  scoreDiff = 0,
  isCoachMode = true,
  onToggleCoachMode,
  onPlayCallSubmitted,
  onOpenFourthDownModal,
  selectedIndex,
  externalCategory,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<PlayCategory>(
    isOffense ? "RUN" : "DEFENSE"
  );
  const [selectedConcept, setSelectedConcept] = useState<TacticalConcept | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [lastSubmittedMessage, setLastSubmittedMessage] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState<boolean>(true);
  const [playClock, setPlayClock] = useState<number>(25);

  // Play Clock Countdown Simulation
  useEffect(() => {
    if (!isCoachMode) return;
    const timer = setInterval(() => {
      setPlayClock((prev) => (prev > 1 ? prev - 1 : 25));
    }, 1000);
    return () => clearInterval(timer);
  }, [isCoachMode]);

  // Sync with externalCategory if provided (e.g. from hotkey 'A')
  useEffect(() => {
    if (externalCategory) {
      setSelectedCategory(externalCategory);
    }
  }, [externalCategory]);

  // Adjust category when possession changes
  useEffect(() => {
    if (isOffense && selectedCategory === "DEFENSE") {
      setSelectedCategory("RUN");
    } else if (!isOffense && (selectedCategory === "RUN" || selectedCategory === "PASS")) {
      setSelectedCategory("DEFENSE");
    }
  }, [isOffense, selectedCategory]);

  const filteredConcepts = TACTICAL_CONCEPTS.filter((c) => c.category === selectedCategory);

  // Sync with selectedIndex from keyboard hotkeys (1-4)
  useEffect(() => {
    if (
      selectedIndex !== undefined &&
      selectedIndex !== null &&
      selectedIndex >= 0 &&
      selectedIndex < filteredConcepts.length
    ) {
      setSelectedConcept(filteredConcepts[selectedIndex]);
    }
  }, [selectedIndex, filteredConcepts]);

  const handleSelectConcept = (concept: TacticalConcept) => {
    soundEffects.playSnap();
    setSelectedConcept(concept);
  };

  const handleSubmitPlay = async () => {
    if (!selectedConcept) return;

    setIsSubmitting(true);
    soundEffects.playWhistle();

    try {
      await apiClient.post("/api/playcalling/call-play", {
        game_id: gameId,
        team_id: teamId,
        play_type: selectedConcept.playType,
        concept_id: selectedConcept.id,
        tempo: "NORMAL",
      });

      setLastSubmittedMessage(`Locked In: ${selectedConcept.name}`);
      if (onPlayCallSubmitted) {
        onPlayCallSubmitted(selectedConcept.playType, selectedConcept.id);
      }

      setTimeout(() => {
        setLastSubmittedMessage(null);
      }, 3500);
    } catch (error) {
      console.warn("Play call submitted with optimistic local execution:", error);
      setLastSubmittedMessage(`Called: ${selectedConcept.name}`);
      if (onPlayCallSubmitted) {
        onPlayCallSubmitted(selectedConcept.playType, selectedConcept.id);
      }
    } finally {
      setIsSubmitting(false);
      setPlayClock(25);
    }
  };

  const getRiskBadge = (risk: string) => {
    switch (risk) {
      case "SAFE":
        return "bg-emerald-950 text-emerald-400 border-emerald-800";
      case "AGGRESSIVE":
        return "bg-red-950 text-red-400 border-red-800";
      default:
        return "bg-amber-950 text-amber-400 border-amber-800";
    }
  };

  return (
    <div className="w-full bg-slate-950/95 border border-white/15 rounded-2xl shadow-2xl backdrop-blur-xl overflow-hidden font-sans text-slate-100">
      {/* Top Controller Header */}
      <div className="flex flex-wrap items-center justify-between px-5 py-3 border-b border-white/10 bg-slate-900/60">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold tracking-wide uppercase text-white">
                Interactive Play-Calling HUD
              </span>
              <span
                className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded font-bold ${
                  isCoachMode ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-slate-800 text-slate-400"
                }`}
              >
                {isCoachMode ? "Coach Mode (User)" : "Spectator Mode (AI)"}
              </span>
            </div>
            <p className="text-[11px] font-mono text-slate-400">
              Down: <strong className="text-white">{down} & {distance}</strong> • Ball:{" "}
              <span className="text-cyan-400">{yardline >= 50 ? `OPP ${100 - yardline}` : `OWN ${yardline}`}</span> • Diff:{" "}
              <span className="text-emerald-400">{scoreDiff > 0 ? `+${scoreDiff}` : scoreDiff}</span> • Play Clock:{" "}
              <span className={`font-bold ${playClock <= 5 ? "text-red-400 animate-ping" : "text-amber-400"}`}>
                :{playClock.toString().padStart(2, "0")}
              </span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Ben Baldwin 4th-Down Button */}
          {down === 4 && onOpenFourthDownModal && (
            <button
              onClick={onOpenFourthDownModal}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-mono text-xs font-bold uppercase rounded-lg shadow-md shadow-emerald-500/20 transition-all animate-pulse"
            >
              <TrendingUp className="w-3.5 h-3.5" />
              Baldwin 4th-Down Model
            </button>
          )}

          {/* Coach Mode Switcher */}
          {onToggleCoachMode && (
            <button
              onClick={() => onToggleCoachMode(!isCoachMode)}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs font-semibold border border-slate-700 transition-colors"
            >
              {isCoachMode ? "Hand to AI" : "Take Command"}
            </button>
          )}

          {/* Expand/Collapse Toggle */}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronUp className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {isExpanded && isCoachMode && (
        <div className="p-4 space-y-4">
          {/* Category Tabs */}
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2">
              {isOffense ? (
                <>
                  <button
                    onClick={() => setSelectedCategory("RUN")}
                    className={`px-4 py-2 rounded-xl text-xs font-bold font-mono tracking-wider uppercase transition-all flex items-center gap-1.5 ${
                      selectedCategory === "RUN"
                        ? "bg-amber-500 text-black shadow-lg shadow-amber-500/20 font-extrabold"
                        : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                    }`}
                  >
                    <Flame className="w-3.5 h-3.5" /> Run Concepts
                    <span className="text-[9px] font-mono ml-1 px-1.5 py-0.5 rounded bg-black/30 border border-black/20 text-white">
                      [A]
                    </span>
                  </button>
                  <button
                    onClick={() => setSelectedCategory("PASS")}
                    className={`px-4 py-2 rounded-xl text-xs font-bold font-mono tracking-wider uppercase transition-all flex items-center gap-1.5 ${
                      selectedCategory === "PASS"
                        ? "bg-cyan-500 text-black shadow-lg shadow-cyan-500/20 font-extrabold"
                        : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                    }`}
                  >
                    <Zap className="w-3.5 h-3.5" /> Pass Concepts
                    <span className="text-[9px] font-mono ml-1 px-1.5 py-0.5 rounded bg-black/30 border border-black/20 text-white">
                      [A]
                    </span>
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setSelectedCategory("DEFENSE")}
                  className={`px-4 py-2 rounded-xl text-xs font-bold font-mono tracking-wider uppercase transition-all flex items-center gap-1.5 ${
                    selectedCategory === "DEFENSE"
                      ? "bg-red-600 text-white shadow-lg shadow-red-600/30 font-extrabold"
                      : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                  }`}
                >
                  <Shield className="w-3.5 h-3.5" /> Defensive Shells
                </button>
              )}
              <button
                onClick={() => setSelectedCategory("SPECIAL_TEAMS")}
                className={`px-4 py-2 rounded-xl text-xs font-bold font-mono tracking-wider uppercase transition-all flex items-center gap-1.5 ${
                  selectedCategory === "SPECIAL_TEAMS"
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 font-extrabold"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                }`}
              >
                <Target className="w-3.5 h-3.5" /> Special Teams
              </button>
            </div>

            {lastSubmittedMessage && (
              <div className="flex items-center gap-1.5 text-xs font-mono text-emerald-400 animate-pulse">
                <CheckCircle className="w-4 h-4" />
                {lastSubmittedMessage}
              </div>
            )}
          </div>

          {/* Tactical Concept Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {filteredConcepts.map((concept, idx) => {
              const isSelected = selectedConcept?.id === concept.id;

              return (
                <div
                  key={concept.id}
                  onClick={() => handleSelectConcept(concept)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between gap-2 ${
                    isSelected
                      ? "bg-cyan-950/80 border-cyan-400 shadow-md shadow-cyan-500/20 scale-[1.02]"
                      : "bg-slate-900/60 border-slate-800/80 hover:bg-slate-800/60 hover:border-slate-700"
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <div className="flex items-center gap-1.5">
                        <span className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono text-[9px] text-cyan-300 font-bold">
                          [{idx + 1}]
                        </span>
                        <span className="font-bold text-xs text-white tracking-wide">
                          {concept.name}
                        </span>
                      </div>
                      <span
                        className={`text-[9px] font-mono px-1.5 py-0.5 rounded border uppercase font-bold ${getRiskBadge(
                          concept.riskReward
                        )}`}
                      >
                        {concept.riskReward}
                      </span>
                    </div>

                    <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                      {concept.description}
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center gap-1 pt-2 border-t border-white/5">
                    {concept.tags.map((tag) => (
                      <span
                        key={tag}
                        className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-300 font-semibold"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Submission Drawer Bar */}
          <div className="pt-2 flex items-center justify-between border-t border-white/10">
            <div className="text-xs font-mono text-slate-400">
              {selectedConcept ? (
                <span>
                  Ready to snap: <strong className="text-white">{selectedConcept.name}</strong> ({selectedConcept.category})
                </span>
              ) : (
                <span>Press [1]-[4] to choose concept • [A] for audible • [T] for timeout</span>
              )}
            </div>

            <button
              onClick={handleSubmitPlay}
              disabled={!selectedConcept || isSubmitting}
              className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-black text-xs font-mono font-bold uppercase tracking-wider rounded-xl shadow-lg shadow-emerald-500/25 transition-all active:scale-95 disabled:opacity-50 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-black" />
              {isSubmitting ? "Transmitting..." : "[SPACE] Snap Ball & Execute Call"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
