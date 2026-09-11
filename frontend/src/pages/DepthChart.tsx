import React, { useState, useEffect, useRef, useMemo } from "react";
import { Reorder, motion, AnimatePresence } from "framer-motion";
import { useLoaderData } from "react-router-dom";
import { ArrowUp, ArrowDown, RotateCcw, Save, CheckCircle2, SlidersHorizontal } from "lucide-react";
import { api } from "../services/api";
import type { Player, Team, ChemistryMetadata } from "../services/api";
import { useTheme } from "../context/useTheme";
import { useSettingsStore } from "../store/useSettingsStore";
import { ChemistryBadge } from "../components/ui/ChemistryBadge";
import { EnhancedPlayerProfile } from "../components/ui/EnhancedPlayerProfile";
import { PlayerAvatar } from "../components/ui/PlayerAvatar";
import { soundEffects } from "../services/soundEffects";

// ============================================================================
// NCAA & MADDEN UNIT / POSITION TAXONOMY
// ============================================================================

export type DepthUnit = "OFFENSE" | "DEFENSE" | "SPECIAL_TEAMS" | "SPECIALISTS";

interface PositionConfig {
  code: string;
  name: string;
  unit: DepthUnit;
  targetCount: number;
  compatiblePositions: string[];
  description: string;
}

const POSITION_CONFIGS: PositionConfig[] = [
  // --- OFFENSE ---
  {
    code: "QB",
    name: "Quarterback",
    unit: "OFFENSE",
    targetCount: 3,
    compatiblePositions: ["QB"],
    description: "Field general orchestrating pre-snap audibles and pass distribution.",
  },
  {
    code: "RB",
    name: "Halfback / RB",
    unit: "OFFENSE",
    targetCount: 3,
    compatiblePositions: ["RB", "FB"],
    description: "Primary ball carrier and zone/gap running weapon.",
  },
  {
    code: "FB",
    name: "Fullback",
    unit: "OFFENSE",
    targetCount: 2,
    compatiblePositions: ["FB", "RB", "TE"],
    description: "Lead blocker in power/I-form sets and short yardage receiver.",
  },
  {
    code: "WR",
    name: "Wide Receiver",
    unit: "OFFENSE",
    targetCount: 5,
    compatiblePositions: ["WR", "TE", "RB"],
    description: "Perimeter route runners and vertical boundary targets.",
  },
  {
    code: "TE",
    name: "Tight End",
    unit: "OFFENSE",
    targetCount: 3,
    compatiblePositions: ["TE", "WR", "FB", "OL"],
    description: "In-line run blocker and middle-of-field seam threat.",
  },
  {
    code: "OT",
    name: "Offensive Tackle (LT/RT)",
    unit: "OFFENSE",
    targetCount: 4,
    compatiblePositions: ["OT", "OL", "OG", "LT", "RT", "C"],
    description: "Edge pass protectors maintaining the pocket perimeter.",
  },
  {
    code: "OG",
    name: "Offensive Guard (LG/RG)",
    unit: "OFFENSE",
    targetCount: 4,
    compatiblePositions: ["OG", "OL", "C", "LG", "RG", "OT"],
    description: "Interior road-graders for inside zone and trap pulling.",
  },
  {
    code: "C",
    name: "Center",
    unit: "OFFENSE",
    targetCount: 2,
    compatiblePositions: ["C", "OL", "OG", "OT"],
    description: "Offensive line captain calling blitz protections and snapping.",
  },

  // --- DEFENSE ---
  {
    code: "DE",
    name: "Defensive End / Edge",
    unit: "DEFENSE",
    targetCount: 4,
    compatiblePositions: ["DE", "LE", "RE", "DL", "EDGE", "LB", "LOLB", "ROLB"],
    description: "Perimeter pass rushers and outside run containment anchors.",
  },
  {
    code: "DT",
    name: "Defensive Tackle / NT",
    unit: "DEFENSE",
    targetCount: 4,
    compatiblePositions: ["DT", "NT", "DL", "DE"],
    description: "Interior trench stalwarts plugging A/B gaps and collapsing the pocket.",
  },
  {
    code: "LB",
    name: "Linebacker (MLB/OLB)",
    unit: "DEFENSE",
    targetCount: 5,
    compatiblePositions: ["LB", "MLB", "LOLB", "ROLB", "DE", "EDGE", "S"],
    description: "Second-level enforcers diagnosing runs and dropping into zone coverage.",
  },
  {
    code: "CB",
    name: "Cornerback",
    unit: "DEFENSE",
    targetCount: 5,
    compatiblePositions: ["CB", "S", "FS", "SS"],
    description: "Boundary island defenders matching outside wideouts in press/man.",
  },
  {
    code: "S",
    name: "Safety (FS/SS)",
    unit: "DEFENSE",
    targetCount: 4,
    compatiblePositions: ["S", "FS", "SS", "CB", "LB"],
    description: "Deep centerfield ball-hawks and box support tacklers.",
  },

  // --- SPECIAL TEAMS ---
  {
    code: "K",
    name: "Placekicker",
    unit: "SPECIAL_TEAMS",
    targetCount: 1,
    compatiblePositions: ["K", "P"],
    description: "Field goal and extra point scoring specialist.",
  },
  {
    code: "P",
    name: "Punter",
    unit: "SPECIAL_TEAMS",
    targetCount: 1,
    compatiblePositions: ["P", "K"],
    description: "Field position tactician delivering high-hangtime directional punts.",
  },
  {
    code: "LS",
    name: "Long Snapper",
    unit: "SPECIAL_TEAMS",
    targetCount: 1,
    compatiblePositions: ["LS", "C", "TE", "OL"],
    description: "Precision snapping specialist for punts and field goal holds.",
  },
  {
    code: "KR",
    name: "Kick Returner",
    unit: "SPECIAL_TEAMS",
    targetCount: 2,
    compatiblePositions: ["WR", "RB", "CB", "S"],
    description: "High-speed return specialist exploiting kickoff lane blocking.",
  },
  {
    code: "PR",
    name: "Punt Returner",
    unit: "SPECIAL_TEAMS",
    targetCount: 2,
    compatiblePositions: ["WR", "CB", "RB", "S"],
    description: "Agile open-field playmaker fielding punts with ball security.",
  },

  // --- SPECIALISTS / SUB PACKAGES (NCAA / MADDEN) ---
  {
    code: "3DRB",
    name: "3rd Down Running Back",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["RB", "WR"],
    description: "Pass-catching back and blitz protection specialist in obvious passing downs.",
  },
  {
    code: "PWHB",
    name: "Power Halfback",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["RB", "FB"],
    description: "Bruising short-yardage and goal-line north-south runner.",
  },
  {
    code: "SLWR",
    name: "Slot Wide Receiver",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["WR", "TE", "RB"],
    description: "Quick-twitch inside receiver attacking soft middle zones in 3+ WR sets.",
  },
  {
    code: "SUBLB",
    name: "Sub Linebacker",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["LB", "MLB", "S", "SS", "FS"],
    description: "High-speed coverage linebacker or safety deployed in Nickel and Dime packages.",
  },
  {
    code: "SLCB",
    name: "Slot Cornerback (Nickel)",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["CB", "S", "FS", "SS"],
    description: "Agile nickelback dedicated to matching up with slot receivers.",
  },
];

const UNIT_TABS: { id: DepthUnit; label: string; icon: string }[] = [
  { id: "OFFENSE", label: "OFFENSE", icon: "🏈" },
  { id: "DEFENSE", label: "DEFENSE", icon: "🛡️" },
  { id: "SPECIAL_TEAMS", label: "SPECIAL TEAMS", icon: "⚡" },
  { id: "SPECIALISTS", label: "SPECIALISTS & SUB", icon: "⭐" },
];

export const DepthChart: React.FC = () => {
  const loaderData = useLoaderData() as
    | { teams?: Team[]; team?: Team; roster?: Player[] }
    | undefined;
  const { activeTeamId, activeTeam, setActiveTeamId } = useTheme();
  const { userTeamId, setUserTeam, fetchSettings } = useSettingsStore();

  const [allTeams, setAllTeams] = useState<Team[]>(loaderData?.teams || []);
  const [selectedTeamId, setSelectedTeamId] = useState<number>(() => {
    if (loaderData?.team?.id) return loaderData.team.id;
    const stored = localStorage.getItem("selectedTeamId");
    if (stored) return parseInt(stored, 10);
    if (userTeamId) return userTeamId;
    return 1;
  });

  const [activeUnit, setActiveUnit] = useState<DepthUnit>("OFFENSE");
  const [selectedPosition, setSelectedPosition] = useState<string>("QB");
  const [roster, setRoster] = useState<Player[]>(loaderData?.roster || []);
  const [positionPlayers, setPositionPlayers] = useState<Player[]>([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [chemistry, setChemistry] = useState<ChemistryMetadata | null>(null);

  // Manual reorder fallback for Playwright E2E and touch devices
  const draggingIdRef = useRef<number | null>(null);
  const isPointerDownRef = useRef(false);

  const endPointerDrag = () => {
    isPointerDownRef.current = false;
    draggingIdRef.current = null;
  };

  useEffect(() => {
    window.addEventListener("pointerup", endPointerDrag);
    window.addEventListener("blur", endPointerDrag);
    return () => {
      window.removeEventListener("pointerup", endPointerDrag);
      window.removeEventListener("blur", endPointerDrag);
    };
  }, []);

  // Sync teams list if not provided by loader
  useEffect(() => {
    fetchSettings();
    if (allTeams.length === 0) {
      api
        .getTeams()
        .then((data) => {
          setAllTeams(data);
        })
        .catch(console.error);
    }
  }, [fetchSettings, allTeams.length]);

  // Sync with activeTeam from ThemeContext or SettingsStore
  useEffect(() => {
    if (allTeams.length > 0) {
      // Find matching team in allTeams based on activeTeamId (e.g. "DET", "GB")
      const matched = allTeams.find(
        (t) => t.abbreviation.toUpperCase() === activeTeamId.toUpperCase()
      );
      if (matched && matched.id !== selectedTeamId) {
        setSelectedTeamId(matched.id);
        localStorage.setItem("selectedTeamId", matched.id.toString());
      }
    }
  }, [activeTeamId, allTeams, selectedTeamId]);

  // Fetch roster & chemistry whenever selectedTeamId changes
  useEffect(() => {
    if (!selectedTeamId) return;

    let isMounted = true;
    const fetchTeamRoster = async () => {
      setLoading(true);
      try {
        const [rosterData, chemData] = await Promise.allSettled([
          api.getTeamRoster(selectedTeamId),
          api.getTeamChemistry(selectedTeamId),
        ]);

        if (isMounted) {
          if (rosterData.status === "fulfilled") {
            setRoster(rosterData.value);
          }
          if (chemData.status === "fulfilled") {
            setChemistry(chemData.value);
          } else {
            setChemistry(null);
          }
        }
      } catch (err) {
        console.error("Failed to load depth chart data for team:", err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchTeamRoster();
    return () => {
      isMounted = false;
    };
  }, [selectedTeamId]);

  // Active position configuration
  const currentPosConfig = useMemo(() => {
    return POSITION_CONFIGS.find((p) => p.code === selectedPosition) || POSITION_CONFIGS[0];
  }, [selectedPosition]);

  // Positions belonging to currently selected unit
  const currentUnitPositions = useMemo(() => {
    return POSITION_CONFIGS.filter((p) => p.unit === activeUnit);
  }, [activeUnit]);

  // Ensure selectedPosition belongs to the activeUnit when tab changes
  useEffect(() => {
    const validInUnit = currentUnitPositions.some((p) => p.code === selectedPosition);
    if (!validInUnit && currentUnitPositions.length > 0) {
      setSelectedPosition(currentUnitPositions[0].code);
    }
  }, [activeUnit, currentUnitPositions, selectedPosition]);

  // Filter and order players for the selected position
  useEffect(() => {
    if (!roster || roster.length === 0) {
      setPositionPlayers([]);
      return;
    }

    const config = currentPosConfig;
    const compatible = config.compatiblePositions;

    // Filter players whose primary position is in compatible list
    const matched = roster.filter((p) => {
      if (p.position === selectedPosition) return true;
      if (compatible.includes(p.position)) return true;
      // Handle generic OL / DL / LB mapping
      if (
        ["LT", "LG", "C", "RG", "RT", "OT", "OG"].includes(selectedPosition) &&
        ["OL", "OT", "OG", "C"].includes(p.position)
      )
        return true;
      if (
        ["DE", "LE", "RE", "DT", "NT"].includes(selectedPosition) &&
        ["DL", "DE", "DT", "EDGE"].includes(p.position)
      )
        return true;
      if (
        ["LOLB", "MLB", "ROLB", "LB", "SUBLB"].includes(selectedPosition) &&
        ["LB", "MLB", "LOLB", "ROLB"].includes(p.position)
      )
        return true;
      if (
        ["CB", "FS", "SS", "S", "SLCB"].includes(selectedPosition) &&
        ["CB", "S", "FS", "SS"].includes(p.position)
      )
        return true;
      return false;
    });

    // Sort: players matching exact code first, then by depth_chart_rank, then overall rating
    matched.sort((a, b) => {
      const aExact = a.position === selectedPosition ? 0 : 1;
      const bExact = b.position === selectedPosition ? 0 : 1;
      if (aExact !== bExact) return aExact - bExact;

      const aRank = a.depth_chart_rank ?? 999;
      const bRank = b.depth_chart_rank ?? 999;
      if (aRank !== bRank) return aRank - bRank;

      return (b.overall_rating || 50) - (a.overall_rating || 50);
    });

    setPositionPlayers(matched);
  }, [roster, selectedPosition, currentPosConfig]);

  // Active Team Object
  const currentTeam = useMemo(() => {
    return (
      allTeams.find((t) => t.id === selectedTeamId) || {
        id: selectedTeamId,
        city: activeTeam?.name?.split(" ")[0] || "Franchise",
        name: activeTeam?.name || "Active Team",
        abbreviation: activeTeamId || "DET",
        conference: activeTeam?.conference || "NFC",
        division: activeTeam?.division || "North",
        wins: 0,
        losses: 0,
        salary_cap_space: 18400000,
      }
    );
  }, [allTeams, selectedTeamId, activeTeam, activeTeamId]);

  // Handle Team Switch
  const handleTeamChange = (newTeamId: number) => {
    soundEffects.playWhistle();
    setSelectedTeamId(newTeamId);
    localStorage.setItem("selectedTeamId", newTeamId.toString());
    setUserTeam(newTeamId);

    const teamObj = allTeams.find((t) => t.id === newTeamId);
    if (teamObj) {
      setActiveTeamId(teamObj.abbreviation);
    }
  };

  // Reorder Handlers
  const handleReorder = (newOrder: Player[]) => {
    setPositionPlayers(newOrder);
  };

  const promotePlayer = (index: number) => {
    if (index <= 0) return;
    soundEffects.playSnap();
    const next = [...positionPlayers];
    const [item] = next.splice(index, 1);
    next.splice(index - 1, 0, item);
    setPositionPlayers(next);
  };

  const demotePlayer = (index: number) => {
    if (index >= positionPlayers.length - 1) return;
    soundEffects.playSnap();
    const next = [...positionPlayers];
    const [item] = next.splice(index, 1);
    next.splice(index + 1, 0, item);
    setPositionPlayers(next);
  };

  const autoReorderByOVR = () => {
    soundEffects.playSnap();
    const sorted = [...positionPlayers].sort(
      (a, b) => (b.overall_rating || 50) - (a.overall_rating || 50)
    );
    setPositionPlayers(sorted);
  };

  const handleReset = async () => {
    soundEffects.playSnap();
    setLoading(true);
    try {
      const data = await api.getTeamRoster(selectedTeamId);
      setRoster(data);
    } catch (e) {
      console.error("Failed to reset roster:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    soundEffects.playCrowdRoar();
    try {
      const playerIds = positionPlayers.map((p) => p.id);
      await api.updateDepthChart(selectedTeamId, selectedPosition, playerIds);

      // Update local roster state
      const updatedRoster = roster.map((p) => {
        const newIndex = playerIds.indexOf(p.id);
        if (newIndex !== -1) {
          return { ...p, depth_chart_rank: newIndex + 1 };
        }
        return p;
      });
      setRoster(updatedRoster);

      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (e) {
      console.error("Failed to save depth chart:", e);
      alert("Failed to save depth chart.");
    } finally {
      setSaving(false);
    }
  };

  // Helper for OVR Badge color tiers
  const getOvrTierClass = (ovr: number) => {
    if (ovr >= 99) {
      return "bg-gradient-to-br from-amber-400 via-yellow-300 to-amber-600 text-black border-amber-300 shadow-lg shadow-amber-500/50";
    }
    if (ovr >= 90) {
      return "bg-gradient-to-br from-cyan-400 via-blue-500 to-indigo-600 text-white border-cyan-300 shadow-lg shadow-cyan-500/40";
    }
    if (ovr >= 80) {
      return "bg-gradient-to-br from-emerald-400 to-green-600 text-white border-emerald-300 shadow-md shadow-emerald-500/30";
    }
    if (ovr >= 70) {
      return "bg-gradient-to-br from-blue-600 to-slate-700 text-white border-blue-400";
    }
    return "bg-slate-800 text-gray-300 border-slate-700";
  };

  const getRankBadge = (index: number) => {
    if (index === 0) {
      return {
        label: "STARTER • 1ST STRING",
        className: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold",
      };
    }
    if (index === 1) {
      return {
        label: "2ND STRING",
        className: "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold",
      };
    }
    if (index === 2) {
      return {
        label: "3RD STRING",
        className: "bg-blue-500/20 text-blue-300 border border-blue-500/40 font-medium",
      };
    }
    return {
      label: `${index + 1}TH STRING`,
      className: "bg-white/10 text-gray-400 border border-white/10 font-normal",
    };
  };

  // Group stats
  const averageGroupOvr = useMemo(() => {
    if (positionPlayers.length === 0) return 0;
    const sum = positionPlayers.reduce((acc, p) => acc + (p.overall_rating || 50), 0);
    return Math.round(sum / positionPlayers.length);
  }, [positionPlayers]);

  const starterPlayer = positionPlayers[0];

  return (
    <div className="p-4 md:p-8 text-white min-h-screen bg-broadcast-dark font-body relative overflow-hidden">
      {/* Background Stadium Carbon Texture */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(16,185,129,0.06),transparent_50%),radial-gradient(ellipse_at_bottom_left,rgba(6,182,212,0.06),transparent_50%)] pointer-events-none" />

      {/* Top Header: Franchise Command & NCAA/Madden Banner */}
      <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-8 pb-6 border-b border-white/10">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold tracking-widest bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 uppercase">
              EA Gridiron 2026 • Roster Hierarchy
            </span>
            <span className="text-gray-400 text-xs font-mono">
              Depth Chart Command & Tactical Rotations
            </span>
          </div>

          <h1 className="text-3xl md:text-4xl font-heading font-black tracking-tight uppercase flex items-center gap-3 text-transparent bg-clip-text bg-gradient-to-r from-white via-gray-100 to-gray-400">
            <span>DEPTH CHART EDITOR</span>
          </h1>
        </div>

        {/* Interactive Franchise Selector */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="bg-white/5 border border-white/10 p-2 rounded-xl backdrop-blur-md flex items-center gap-3">
            <img
              src={`/logos/${currentTeam.abbreviation}.png`}
              alt={currentTeam.name}
              className="w-10 h-10 object-contain drop-shadow-[0_0_8px_rgba(255,255,255,0.2)]"
              onError={(e) => {
                (e.target as HTMLElement).style.display = "none";
              }}
            />
            <div>
              <div className="text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-wider">
                ACTIVE FRANCHISE
              </div>
              <select
                value={selectedTeamId}
                onChange={(e) => handleTeamChange(Number(e.target.value))}
                className="bg-transparent text-white font-heading font-bold text-base focus:outline-none cursor-pointer pr-4"
              >
                {allTeams.map((t) => (
                  <option key={t.id} value={t.id} className="bg-slate-900 text-white">
                    {t.city} {t.name} ({t.abbreviation})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Quick Action Toolbar */}
          <div className="flex items-center gap-2">
            <button
              onClick={autoReorderByOVR}
              title="Auto-sort position depth by overall rating"
              className="px-3.5 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-mono font-semibold text-gray-300 hover:text-white transition-all flex items-center gap-2"
            >
              <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
              <span className="hidden sm:inline">Auto-Order OVR</span>
            </button>

            <button
              onClick={handleReset}
              title="Reset depth chart to database state"
              className="px-3.5 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-mono font-semibold text-gray-300 hover:text-white transition-all flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4 text-amber-400" />
              <span className="hidden sm:inline">Reset</span>
            </button>

            <button
              onClick={handleSave}
              disabled={saving}
              className="px-5 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-500 hover:to-green-400 text-white text-xs font-heading font-black tracking-wider uppercase disabled:opacity-50 transition-all shadow-lg shadow-emerald-900/30 flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? "Saving..." : "Save Changes"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Save Success Alert Banner */}
      <AnimatePresence>
        {saveSuccess && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-6 p-4 rounded-xl bg-emerald-950/80 border border-emerald-500 text-emerald-200 flex items-center gap-3 backdrop-blur-md shadow-lg shadow-emerald-950/50"
          >
            <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
            <div className="text-sm font-semibold">
              Depth chart for <span className="font-bold text-white">{selectedPosition}</span>{" "}
              successfully updated and synced across game sim engines!
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 4-Unit Master Navigation Bar (NCAA 25 / Madden 25 Style) */}
      <div className="relative z-10 mb-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 bg-black/40 p-1.5 rounded-2xl border border-white/10 backdrop-blur-xl">
          {UNIT_TABS.map((tab) => {
            const isActive = activeUnit === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  soundEffects.playSnap();
                  setActiveUnit(tab.id);
                }}
                className={`relative py-3 px-4 rounded-xl flex items-center justify-center gap-2 font-heading font-black tracking-wide text-xs sm:text-sm uppercase transition-all duration-300 ${
                  isActive
                    ? "bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg shadow-cyan-900/40 border border-cyan-400/40"
                    : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
                }`}
              >
                <span className="text-base">{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Position Pill Bar */}
      <div className="relative z-10 mb-6 overflow-x-auto pb-2 scrollbar-thin">
        <div className="flex gap-2 min-w-max">
          {currentUnitPositions.map((pos) => {
            const isSelected = selectedPosition === pos.code;
            // Count players in this slot
            const count = roster.filter((p) => {
              if (p.position === pos.code) return true;
              if (pos.compatiblePositions.includes(p.position)) return true;
              return false;
            }).length;

            return (
              <button
                key={pos.code}
                onClick={() => {
                  soundEffects.playSnap();
                  setSelectedPosition(pos.code);
                }}
                className={`px-4 py-2.5 rounded-xl text-xs font-mono font-bold uppercase transition-all duration-200 flex items-center gap-2.5 ${
                  isSelected
                    ? "bg-cyan-500 text-black font-black shadow-lg shadow-cyan-500/30 scale-105"
                    : "bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white border border-white/5"
                }`}
              >
                <span>{pos.code}</span>
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded-md font-mono ${
                    isSelected ? "bg-black/30 text-white" : "bg-white/10 text-gray-400"
                  }`}
                >
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Grid: Position Room Dossier & Interactive Reorder List */}
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Position Room Summary & Tactics (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-black/40 border border-white/10 rounded-2xl p-6 backdrop-blur-xl shadow-2xl">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <span className="text-2xl font-black font-heading text-cyan-400">
                  {currentPosConfig.code}
                </span>
                <span className="text-gray-300 font-bold text-sm">{currentPosConfig.name}</span>
              </div>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-white/10 text-cyan-300 border border-white/10">
                {currentPosConfig.unit}
              </span>
            </div>

            <p className="text-xs text-gray-400 mb-6 leading-relaxed">
              {currentPosConfig.description}
            </p>

            {/* Room Metrics */}
            <div className="grid grid-cols-2 gap-3 mb-6">
              <div className="bg-white/5 border border-white/5 rounded-xl p-3">
                <div className="text-[10px] font-mono text-gray-400 uppercase">ROOM AVERAGE</div>
                <div className="text-2xl font-black font-heading text-white mt-1">
                  {averageGroupOvr} <span className="text-xs text-cyan-400 font-mono">OVR</span>
                </div>
              </div>
              <div className="bg-white/5 border border-white/5 rounded-xl p-3">
                <div className="text-[10px] font-mono text-gray-400 uppercase">
                  ACTIVE AT POSITION
                </div>
                <div className="text-2xl font-black font-heading text-emerald-400 mt-1">
                  {positionPlayers.length}{" "}
                  <span className="text-xs text-gray-400 font-mono">
                    / {currentPosConfig.targetCount} Target
                  </span>
                </div>
              </div>
            </div>

            {/* Starter Spotlight Card */}
            {starterPlayer && (
              <div className="bg-gradient-to-br from-white/10 to-white/5 border border-white/15 rounded-xl p-4 mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-mono text-emerald-400 font-bold tracking-widest uppercase">
                    ★ CURRENT STARTER (RANK 1)
                  </span>
                  <span className="text-xs font-mono text-gray-400">
                    #{starterPlayer.jersey_number}
                  </span>
                </div>
                <div className="text-lg font-heading font-black text-white">
                  {starterPlayer.first_name} {starterPlayer.last_name}
                </div>
                <div className="text-xs text-gray-300 mt-1 flex items-center gap-3">
                  <span>OVR {starterPlayer.overall_rating}</span>
                  <span>•</span>
                  <span>{starterPlayer.college || "NFL Veteran"}</span>
                  <span>•</span>
                  <span>{starterPlayer.experience} Yrs</span>
                </div>
              </div>
            )}

            {/* Unit Chemistry Integration (Offensive Line / Defensive Line) */}
            {["OT", "OG", "C", "LT", "LG", "RG", "RT"].includes(selectedPosition) && chemistry && (
              <div className="p-4 rounded-xl bg-cyan-950/30 border border-cyan-500/30">
                <div className="text-xs font-bold text-cyan-300 uppercase tracking-wider mb-2 flex items-center gap-2">
                  <span>⚗️ Unit Chemistry Synergy</span>
                </div>
                <ChemistryBadge
                  level={chemistry.chemistry_level}
                  consecutiveGames={chemistry.consecutive_games}
                  status={chemistry.status}
                  bonuses={chemistry.bonuses}
                />
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Interactive Reorderable Depth List (8 Cols) */}
        <div className="lg:col-span-8">
          <div className="bg-black/40 border border-white/10 rounded-2xl p-6 backdrop-blur-xl shadow-2xl">
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
              <div>
                <h2 className="text-xl font-heading font-black text-white tracking-wide uppercase">
                  {selectedPosition} Depth Chart
                </h2>
                <p className="text-xs text-gray-400 mt-0.5">
                  Drag athletes or use ▲/▼ buttons to set rotational depth for live game sim.
                </p>
              </div>

              <div className="text-xs font-mono text-gray-400">
                {positionPlayers.length} Athletes Loaded
              </div>
            </div>

            {loading ? (
              <div className="py-16 text-center text-gray-400 font-mono flex flex-col items-center justify-center gap-3">
                <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
                <span>Loading Roster...</span>
              </div>
            ) : positionPlayers.length === 0 ? (
              <div className="py-16 text-center border-2 border-dashed border-white/10 rounded-xl text-gray-500 font-mono">
                No players currently assigned to {selectedPosition}. Use "+ Add Athlete" to assign
                players from your 53-man roster.
              </div>
            ) : (
              <Reorder.Group
                as="div"
                axis="y"
                values={positionPlayers}
                onReorder={handleReorder}
                className="Reorder_Group space-y-3"
              >
                {positionPlayers.map((player, index) => {
                  const rankBadge = getRankBadge(index);
                  const ovrClass = getOvrTierClass(player.overall_rating || 50);

                  return (
                    <Reorder.Item
                      as="div"
                      key={player.id}
                      value={player}
                      dragListener={false}
                      style={{ touchAction: "none" }}
                      onPointerDown={() => {
                        isPointerDownRef.current = true;
                        draggingIdRef.current = player.id;
                      }}
                      onPointerEnter={() => {
                        if (!isPointerDownRef.current) return;
                        const draggingId = draggingIdRef.current;
                        if (!draggingId || draggingId === player.id) return;

                        setPositionPlayers((prev) => {
                          const fromIndex = prev.findIndex((p) => p.id === draggingId);
                          const toIndex = prev.findIndex((p) => p.id === player.id);
                          if (fromIndex === -1 || toIndex === -1 || fromIndex === toIndex)
                            return prev;

                          const next = [...prev];
                          const [moved] = next.splice(fromIndex, 1);
                          next.splice(toIndex, 0, moved);
                          return next;
                        });
                      }}
                      className={`bg-white/5 p-4 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-grab active:cursor-grabbing hover:bg-white/10 border transition-all duration-200 group ${
                        index === 0 ? "border-emerald-500/30 bg-emerald-950/10" : "border-white/5"
                      }`}
                    >
                      {/* Left: Rank, OVR Shield, Name, Specs */}
                      <div className="flex items-center gap-4">
                        {/* Rank Badge Indicator */}
                        <div className="flex flex-col items-center justify-center min-w-[3rem]">
                          <div className="text-xl font-heading font-black text-gray-200">
                            #{index + 1}
                          </div>
                          <span
                            className={`text-[9px] px-1.5 py-0.2 rounded mt-0.5 ${rankBadge.className}`}
                          >
                            {index === 0 ? "STARTER" : `STR ${index + 1}`}
                          </span>
                        </div>

                        {/* Player Avatar */}
                        <PlayerAvatar
                          playerId={player.id}
                          teamAbbr={currentTeam.abbreviation}
                          pose="headshot"
                          size="md"
                          position={player.position}
                          jerseyNumber={player.jersey_number}
                          playerName={`${player.first_name} ${player.last_name}`}
                          className="flex-shrink-0"
                        />

                        {/* Metallic OVR Shield */}
                        <div
                          className={`w-12 h-12 rounded-xl flex flex-col items-center justify-center border font-heading font-black flex-shrink-0 ${ovrClass}`}
                        >
                          <span className="text-lg leading-none">
                            {player.overall_rating || 50}
                          </span>
                          <span className="text-[9px] font-mono tracking-tighter opacity-80 uppercase">
                            OVR
                          </span>
                        </div>

                        {/* Player Details */}
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-heading font-bold text-lg text-gray-100 group-hover:text-cyan-300 transition-colors">
                              {player.first_name} {player.last_name}
                            </span>
                            <span className="text-xs font-mono text-gray-400">
                              #{player.jersey_number}
                            </span>
                            {player.position !== selectedPosition && (
                              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                                Nat: {player.position}
                              </span>
                            )}
                          </div>

                          <div className="text-xs text-gray-400 flex flex-wrap items-center gap-2 sm:gap-3 mt-1">
                            <span>Age {player.age}</span>
                            <span>•</span>
                            <span>
                              {player.height
                                ? `${Math.floor(player.height / 12)}'${player.height % 12}"`
                                : "6'1\""}
                            </span>
                            <span>{player.weight ? `${player.weight} lbs` : "215 lbs"}</span>
                            <span>•</span>
                            <span>{player.college || "NCAA"}</span>
                          </div>

                          {/* Attribute Chips */}
                          <div className="flex items-center gap-2 mt-2">
                            <span className="text-[10px] font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5 text-gray-300">
                              SPD: <strong className="text-cyan-400">{player.speed || 80}</strong>
                            </span>
                            <span className="text-[10px] font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5 text-gray-300">
                              ACC:{" "}
                              <strong className="text-cyan-400">{player.acceleration || 80}</strong>
                            </span>
                            <span className="text-[10px] font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5 text-gray-300">
                              STR:{" "}
                              <strong className="text-cyan-400">{player.strength || 75}</strong>
                            </span>
                            <span className="text-[10px] font-mono bg-white/5 px-2 py-0.5 rounded border border-white/5 text-gray-300">
                              AWR:{" "}
                              <strong className="text-cyan-400">{player.awareness || 78}</strong>
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Right: Promote/Demote controls, Dossier button, Drag Handle */}
                      <div className="flex items-center justify-end gap-2">
                        {/* Promote / Demote Buttons */}
                        <div className="flex items-center bg-black/40 rounded-lg p-0.5 border border-white/10">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              promotePlayer(index);
                            }}
                            disabled={index === 0}
                            className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded disabled:opacity-20 transition-colors"
                            title="Promote player in depth chart"
                          >
                            <ArrowUp className="w-4 h-4 text-emerald-400" />
                          </button>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              demotePlayer(index);
                            }}
                            disabled={index === positionPlayers.length - 1}
                            className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded disabled:opacity-20 transition-colors"
                            title="Demote player in depth chart"
                          >
                            <ArrowDown className="w-4 h-4 text-amber-400" />
                          </button>
                        </div>

                        {/* Dossier Button */}
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedPlayerId(player.id);
                          }}
                          className="px-3 py-1.5 rounded-lg bg-cyan-950/80 border border-cyan-700 text-cyan-300 hover:text-white hover:bg-cyan-800 text-xs font-mono font-semibold transition-all shadow-sm"
                          title="Inspect Detailed Player Dossier"
                        >
                          Dossier
                        </button>

                        {/* Drag Handle Icon */}
                        <div className="text-white/20 group-hover:text-white/60 cursor-grab p-1">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          >
                            <circle cx="9" cy="12" r="1" />
                            <circle cx="9" cy="5" r="1" />
                            <circle cx="9" cy="19" r="1" />
                            <circle cx="15" cy="12" r="1" />
                            <circle cx="15" cy="5" r="1" />
                            <circle cx="15" cy="19" r="1" />
                          </svg>
                        </div>
                      </div>
                    </Reorder.Item>
                  );
                })}
              </Reorder.Group>
            )}
          </div>
        </div>
      </div>

      {/* Enhanced Player Profile Dossier Modal */}
      {selectedPlayerId && (
        <EnhancedPlayerProfile
          playerId={selectedPlayerId}
          onClose={() => setSelectedPlayerId(null)}
        />
      )}
    </div>
  );
};

export default DepthChart;
