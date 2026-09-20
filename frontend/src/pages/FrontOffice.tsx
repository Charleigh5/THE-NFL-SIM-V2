import React, { useEffect, useState, useMemo } from "react";
import { EnhancedPlayerProfile } from "../components/ui/EnhancedPlayerProfile";
import CoachSettings from "../components/coaching/CoachSettings";
import { SpatialSceneViewport } from "../components/spatial/SpatialSceneViewport";
import { SpatialAtmosphereLayer } from "../components/spatial/SpatialAtmosphereLayer";
import { PlayerAvatar } from "../components/ui/PlayerAvatar";
import { api } from "../services/api";
import { useTheme } from "../context/useTheme";
import { soundEffects } from "../services/soundEffects";
import type { Player, Team } from "../services/api";
import {
  Users,
  Filter,
  ArrowUpDown,
  DollarSign,
  X,
  Table as TableIcon,
  Shield,
  ClipboardList,
  Award,
} from "lucide-react";
import {
  VirtualizedTable,
  type VirtualizedTableColumn,
} from "../components/common/VirtualizedTable";

export type FrontOfficeMode = "lockers" | "office" | "table";

type PositionFilter =
  | "ALL"
  | "OFF"
  | "DEF"
  | "ST"
  | "QB"
  | "RB"
  | "WR"
  | "TE"
  | "OL"
  | "DL"
  | "LB"
  | "DB"
  | "K/P";

type SortOption = "OVR" | "AGE" | "SPEED" | "STRENGTH";

const LOCKER_PARALLAX = {
  maxOffsetX: 14,
  maxOffsetY: 8,
  maxRotateX: 1.8,
  maxRotateY: 2.5,
};

const OFFICE_PARALLAX = {
  maxOffsetX: 16,
  maxOffsetY: 10,
  maxRotateX: 2.2,
  maxRotateY: 3.0,
};

interface LockerStallCardProps {
  player: Player;
  teamAbbr?: string;
  onClick: () => void;
}

/**
 * First-Person Honolulu Blue Player Locker Stall
 * Designed under Adly Frontier UI Architect principles with metallic brushed nameplates,
 * crisp corner radius, Honolulu Blue (#0076B6) framing, and deterministic interactive states.
 */
const LockerStallCard: React.FC<LockerStallCardProps> = ({ player, teamAbbr = "DET", onClick }) => {
  const ovr = player.overall_rating;
  const ovrBadgeStyle =
    ovr >= 90
      ? "from-amber-400 to-yellow-500 text-black shadow-amber-500/30"
      : ovr >= 80
        ? "from-emerald-400 to-teal-500 text-black shadow-emerald-500/30"
        : ovr >= 70
          ? "from-cyan-400 to-blue-500 text-black shadow-cyan-500/30"
          : "from-zinc-400 to-zinc-500 text-black shadow-zinc-500/30";

  return (
    <div
      role="button"
      tabIndex={0}
      data-testid={`player-card-${player.id}`}
      onClick={() => {
        soundEffects.playLockerDoorLatch();
        onClick();
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          soundEffects.playLockerDoorLatch();
          onClick();
        }
      }}
      className="group relative flex flex-col rounded-lg overflow-hidden border border-[#0076B6]/40 hover:border-[#0076B6] bg-gradient-to-b from-[#06101e] via-[#040810] to-[#020306] shadow-xl hover:shadow-[0_0_24px_rgba(0,118,182,0.4)] transition-all duration-200 cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#0076B6] active:scale-[0.98]"
    >
      {/* Metallic Brushed Aluminum Nameplate Header with Rivet Corners */}
      <div className="relative bg-gradient-to-r from-zinc-700 via-zinc-400 to-zinc-700 p-[1px] shadow-inner">
        <div className="bg-gradient-to-r from-zinc-900 via-zinc-800 to-zinc-900 px-3 py-1.5 flex items-center justify-between border-b border-zinc-600/80">
          {/* Rivet Left + Player Jersey & Name */}
          <div className="flex items-center gap-2 min-w-0">
            <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 border border-zinc-900 shadow-sm shrink-0" />
            <span className="font-header text-xs tracking-wider text-white uppercase font-bold truncate">
              #{player.jersey_number ?? 0} {player.last_name}
            </span>
          </div>

          {/* OVR Badge + Rivet Right */}
          <div className="flex items-center gap-2 shrink-0">
            <div
              className={`px-1.5 py-0.5 rounded font-header font-black text-xs uppercase tracking-tight shadow-md bg-gradient-to-r ${ovrBadgeStyle}`}
            >
              {ovr} <span className="text-[9px] font-mono font-bold">OVR</span>
            </div>
            <span className="w-1.5 h-1.5 rounded-full bg-zinc-400 border border-zinc-900 shadow-sm shrink-0" />
          </div>
        </div>
      </div>

      {/* Locker Stall Cavity Interior */}
      <div className="relative p-4 flex flex-col items-center justify-between flex-1 min-h-[220px] overflow-hidden">
        {/* Background Honolulu Blue Giant Number Watermark */}
        <span className="absolute -right-2 -bottom-3 font-header font-black italic text-7xl text-[#0076B6]/15 select-none pointer-events-none -skew-x-12">
          #{player.jersey_number ?? 0}
        </span>

        {/* Top Slotted Locker Air Vents */}
        <div className="w-full flex justify-center gap-1.5 mb-3 opacity-60">
          <span className="h-1 w-6 bg-white/10 rounded-full" />
          <span className="h-1 w-6 bg-white/10 rounded-full" />
          <span className="h-1 w-6 bg-white/10 rounded-full" />
        </div>

        {/* Player Avatar in Locker Gear */}
        <div className="relative my-1">
          <div className="w-20 h-20 rounded-lg overflow-hidden border-2 border-[#0076B6]/50 shadow-[0_0_16px_rgba(0,118,182,0.3)] group-hover:border-[#0076B6] group-hover:scale-105 transition-all bg-slate-900">
            <PlayerAvatar
              playerId={player.id}
              teamAbbr={teamAbbr}
              pose="headshot"
              size="lg"
              position={player.position}
              jerseyNumber={player.jersey_number}
              playerName={`${player.first_name} ${player.last_name}`}
              className="w-full h-full"
              primaryColor="#0076B6"
            />
          </div>
          <span className="absolute -bottom-2 left-1/2 -translate-x-1/2 px-2 py-0.5 rounded bg-[#0076B6] border border-cyan-400 text-white font-mono text-[10px] font-bold tracking-wider shadow-md">
            {player.position}
          </span>
        </div>

        {/* Player Identity */}
        <div className="text-center mt-3 mb-2 z-10">
          <h3 className="font-header text-base uppercase tracking-tight text-white group-hover:text-cyan-300 transition-colors leading-tight">
            {player.first_name} {player.last_name}
          </h3>
          <p className="text-[10px] font-mono text-gray-400 mt-0.5">
            {player.college || "NFL Veteran"} • {player.experience ?? 0} yrs
          </p>
        </div>

        {/* Athletic Stat Bar Breakdown */}
        <div className="w-full grid grid-cols-3 gap-1.5 pt-2 border-t border-white/10 text-center font-mono z-10">
          <div className="bg-black/50 p-1.5 rounded border border-white/5">
            <span className="text-[9px] text-gray-400 uppercase block leading-none mb-1">SPD</span>
            <span className="font-bold text-xs text-emerald-400 leading-none">
              {player.speed ?? 85}
            </span>
          </div>
          <div className="bg-black/50 p-1.5 rounded border border-white/5">
            <span className="text-[9px] text-gray-400 uppercase block leading-none mb-1">STR</span>
            <span className="font-bold text-xs text-cyan-400 leading-none">
              {player.strength ?? 80}
            </span>
          </div>
          <div className="bg-black/50 p-1.5 rounded border border-white/5">
            <span className="text-[9px] text-gray-400 uppercase block leading-none mb-1">AGI</span>
            <span className="font-bold text-xs text-amber-400 leading-none">
              {player.agility ?? 84}
            </span>
          </div>
        </div>

        {/* Locker Shelf Action Tag */}
        <div className="w-full mt-3 pt-2 flex items-center justify-between text-[11px] font-mono text-cyan-300/80 group-hover:text-cyan-200 transition-colors border-t border-[#0076B6]/20 z-10">
          <span className="flex items-center gap-1">
            <Shield size={11} className="text-[#0076B6]" />
            Stall #{player.jersey_number ?? 0}
          </span>
          <span className="font-header uppercase tracking-wider text-[10px] text-[#0076B6] group-hover:text-cyan-300">
            Dossier &rarr;
          </span>
        </div>
      </div>
    </div>
  );
};

interface DanCampbellWhiteboardProps {
  opponentName?: string;
  week?: number;
}

/**
 * Dan Campbell Dynamic Whiteboard
 * ===============================
 * Tactical game-plan chalkboard/notepad detailing keys to victory for the upcoming week.
 * Styled with metallic dry-erase framing, Adly Frontier UI Architect aesthetics,
 * and high-contrast tactical football directives.
 */
const DanCampbellWhiteboard: React.FC<DanCampbellWhiteboardProps> = ({
  opponentName = "OPPONENT",
  week = 5,
}) => {
  return (
    <div
      data-testid="dan-campbell-whiteboard"
      className="relative rounded-xl overflow-hidden border-2 border-zinc-700 bg-gradient-to-b from-[#0e1724] via-[#09101a] to-[#05090f] p-5 shadow-2xl shadow-black/80"
    >
      {/* Aluminum Board Frame Header with Rivets */}
      <div className="flex flex-wrap items-center justify-between pb-3 mb-4 border-b border-white/15 gap-2">
        <div className="flex items-center gap-2.5">
          <span className="w-3 h-3 rounded-full bg-red-500 shadow-md shadow-red-500/50 animate-pulse" />
          <div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-yellow-400 font-bold block">
              Allen Park Command Tactical Whiteboard &bull; Dan Campbell Game Plan
            </span>
            <h3 className="font-header text-xl sm:text-2xl uppercase tracking-wider text-white">
              WEEK {week} VS {opponentName}: KEYS TO VICTORY
            </h3>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 rounded bg-black/60 border border-[#0076B6]/40 font-mono text-[10px] text-cyan-300 font-bold uppercase tracking-wider">
            ALL GRIT &bull; 100%
          </span>
        </div>
      </div>

      {/* Chalkboard / Whiteboard Tactical Directives */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
        {/* Key 1 */}
        <div className="p-3.5 rounded-lg bg-black/55 border-l-4 border-red-500 border-t border-r border-b border-white/10 space-y-1.5 shadow-lg">
          <div className="flex items-center justify-between">
            <span className="text-red-400 font-bold font-header text-sm tracking-wide">
              1. ATTACK A-GAP MUG FRONTS
            </span>
            <span className="text-[9px] px-1.5 py-0.5 rounded bg-red-500/20 text-red-300 font-bold uppercase">
              DEF FRONT
            </span>
          </div>
          <p className="text-gray-300 leading-relaxed font-body text-xs">
            Overload interior protection with double A-gap mug alignments. Disguise 5-man creepers
            on 3rd down and collapse the pocket.
          </p>
          <div className="text-[10px] text-gray-400 pt-1.5 border-t border-white/10 flex justify-between font-mono">
            <span>Pressure Win Rate:</span>
            <span className="text-red-400 font-bold">38.5%+</span>
          </div>
        </div>

        {/* Key 2 */}
        <div className="p-3.5 rounded-lg bg-black/55 border-l-4 border-amber-500 border-t border-r border-b border-white/10 space-y-1.5 shadow-lg">
          <div className="flex items-center justify-between">
            <span className="text-amber-400 font-bold font-header text-sm tracking-wide">
              2. 4TH & 2 OR LESS = 100% GO
            </span>
            <span className="text-[9px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold uppercase">
              ATTACK
            </span>
          </div>
          <p className="text-gray-300 leading-relaxed font-body text-xs">
            Zero hesitation across midfield. We dictate the terms and impose physical will.
            Short-yardage wedge sneak with heavy personnel.
          </p>
          <div className="text-[10px] text-gray-400 pt-1.5 border-t border-white/10 flex justify-between font-mono">
            <span>Aggression Index:</span>
            <span className="text-amber-400 font-bold">#1 NFL (88%)</span>
          </div>
        </div>

        {/* Key 3 */}
        <div className="p-3.5 rounded-lg bg-black/55 border-l-4 border-cyan-500 border-t border-r border-b border-white/10 space-y-1.5 shadow-lg">
          <div className="flex items-center justify-between">
            <span className="text-cyan-400 font-bold font-header text-sm tracking-wide">
              3. ESTABLISH 12-PERSONNEL POWER RUN
            </span>
            <span className="text-[9px] px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-bold uppercase">
              GROUND
            </span>
          </div>
          <p className="text-gray-300 leading-relaxed font-body text-xs">
            Double-team the 3-technique, pull the backside guard on Counter GT, and chew 4.8 YPC.
            Set up deep explosive post shot off play-action.
          </p>
          <div className="text-[10px] text-gray-400 pt-1.5 border-t border-white/10 flex justify-between font-mono">
            <span>Downhill Target:</span>
            <span className="text-cyan-400 font-bold">140+ YDS</span>
          </div>
        </div>
      </div>

      {/* Handwritten Dry-Erase Footer Quote */}
      <div className="mt-4 pt-3 border-t border-white/10 flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-gray-400">
        <span className="italic text-yellow-300/90 font-semibold">
          &ldquo;When you get knocked down, you get up and bite off a kneecap. That's who we
          are.&rdquo; &mdash; Coach Dan Campbell
        </span>
        <span className="text-cyan-400 font-bold uppercase tracking-wider">
          STATUS: GAMEDAY LOCKED IN
        </span>
      </div>
    </div>
  );
};

export const FrontOffice: React.FC = () => {
  const [roster, setRoster] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [enhancedPlayerId, setEnhancedPlayerId] = useState<number | null>(null);
  const [team, setTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [positionFilter, setPositionFilter] = useState<PositionFilter>("ALL");
  const [sortBy, setSortBy] = useState<SortOption>("OVR");

  // Tri-Mode Spatial Controller: 'lockers' | 'office' | 'table'
  const [mode, setMode] = useState<FrontOfficeMode>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("nfl_sim_front_office_mode") as FrontOfficeMode | null;
      if (saved === "lockers" || saved === "office" || saved === "table") {
        return saved;
      }
    }
    return "lockers";
  });

  const { activeTeam } = useTheme();

  const handleModeChange = (newMode: FrontOfficeMode) => {
    soundEffects.playSnap?.();
    setMode(newMode);
    try {
      localStorage.setItem("nfl_sim_front_office_mode", newMode);
    } catch (err) {
      console.error("Failed to persist front office mode", err);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const teamData = await api.getTeam(1);
        const rosterData = await api.getTeamRoster(1);
        setTeam(teamData);
        setRoster(rosterData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredAndSortedRoster = useMemo(() => {
    let list = [...roster];

    // Filter
    if (positionFilter === "OFF") {
      list = list.filter((p) =>
        ["QB", "RB", "WR", "TE", "OT", "OG", "C", "LT", "LG", "RG", "RT"].includes(p.position)
      );
    } else if (positionFilter === "DEF") {
      list = list.filter((p) =>
        ["DE", "DT", "LB", "MLB", "OLB", "CB", "S", "FS", "SS"].includes(p.position)
      );
    } else if (positionFilter === "ST") {
      list = list.filter((p) => ["K", "P", "LS"].includes(p.position));
    } else if (positionFilter === "OL") {
      list = list.filter((p) => ["OT", "OG", "C", "LT", "LG", "RG", "RT"].includes(p.position));
    } else if (positionFilter === "DL") {
      list = list.filter((p) => ["DE", "DT"].includes(p.position));
    } else if (positionFilter === "DB") {
      list = list.filter((p) => ["CB", "S", "FS", "SS"].includes(p.position));
    } else if (positionFilter === "K/P") {
      list = list.filter((p) => ["K", "P", "LS"].includes(p.position));
    } else if (positionFilter !== "ALL") {
      list = list.filter((p) => p.position === positionFilter);
    }

    // Sort
    list.sort((a, b) => {
      if (sortBy === "OVR") return (b.overall_rating || 0) - (a.overall_rating || 0);
      if (sortBy === "AGE") return (a.age || 0) - (b.age || 0);
      if (sortBy === "SPEED") return (b.speed || 0) - (a.speed || 0);
      if (sortBy === "STRENGTH") return (b.strength || 0) - (a.strength || 0);
      return 0;
    });

    return list;
  }, [roster, positionFilter, sortBy]);

  // Virtualized Table Columns for 53-man roster view (Editorial Monograph Aesthetics)
  const tableColumns: VirtualizedTableColumn<Player>[] = useMemo(
    () => [
      {
        id: "jersey",
        header: "#",
        width: 60,
        align: "center",
        sortable: true,
        sortKey: (p) => p.jersey_number,
        cell: (p) => (
          <span
            data-testid={`player-card-${p.id}`}
            className="font-header text-sm text-yellow-400 font-bold"
          >
            #{p.jersey_number ?? 0}
          </span>
        ),
      },
      {
        id: "name",
        header: "Player Name",
        minWidth: 160,
        sortable: true,
        sortKey: (p) => `${p.first_name} ${p.last_name}`,
        cell: (p) => (
          <div className="flex flex-col">
            <span className="font-header text-sm text-white uppercase tracking-tight">
              {p.first_name} {p.last_name}
            </span>
            <span className="text-[10px] font-mono text-gray-400">
              {p.college || "NFL Veteran"}
            </span>
          </div>
        ),
      },
      {
        id: "position",
        header: "Pos",
        width: 65,
        align: "center",
        sortable: true,
        sortKey: (p) => p.position,
        cell: (p) => (
          <span className="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-white font-mono text-xs font-bold">
            {p.position}
          </span>
        ),
      },
      {
        id: "overall",
        header: "OVR",
        width: 65,
        align: "center",
        sortable: true,
        sortKey: (p) => p.overall_rating,
        cell: (p) => {
          const ovr = p.overall_rating;
          const ratingColor =
            ovr >= 90
              ? "text-yellow-400 font-bold"
              : ovr >= 80
                ? "text-emerald-400 font-semibold"
                : ovr >= 70
                  ? "text-cyan-400"
                  : "text-gray-300";
          return <span className={`text-base font-header ${ratingColor}`}>{ovr}</span>;
        },
      },
      {
        id: "age",
        header: "Age",
        width: 55,
        align: "center",
        sortable: true,
        sortKey: (p) => p.age,
        cell: (p) => <span className="text-gray-300 font-mono text-xs">{p.age}</span>,
      },
      {
        id: "exp",
        header: "Exp",
        width: 65,
        align: "center",
        sortable: true,
        sortKey: (p) => p.experience,
        cell: (p) => (
          <span className="text-gray-400 font-mono text-xs">{p.experience ?? 0} yrs</span>
        ),
      },
      {
        id: "speed",
        header: "SPD",
        width: 60,
        align: "center",
        sortable: true,
        sortKey: (p) => p.speed,
        cell: (p) => (
          <span className="text-emerald-400 font-mono text-xs font-bold">{p.speed ?? 85}</span>
        ),
      },
      {
        id: "strength",
        header: "STR",
        width: 60,
        align: "center",
        sortable: true,
        sortKey: (p) => p.strength,
        cell: (p) => (
          <span className="text-cyan-400 font-mono text-xs font-bold">{p.strength ?? 80}</span>
        ),
      },
      {
        id: "agility",
        header: "AGI",
        width: 60,
        align: "center",
        sortable: true,
        sortKey: (p) => p.agility,
        cell: (p) => (
          <span className="text-amber-400 font-mono text-xs font-bold">{p.agility ?? 84}</span>
        ),
      },
      {
        id: "actions",
        header: "Action",
        width: 90,
        align: "center",
        cell: (p) => (
          <button
            onClick={(e) => {
              e.stopPropagation();
              soundEffects.playSnap?.();
              setSelectedPlayer(p);
            }}
            className="px-2.5 py-1 bg-white/10 hover:bg-[#0076B6]/30 hover:border-[#0076B6]/50 text-gray-200 hover:text-white font-header text-[11px] uppercase tracking-wider rounded border border-white/5 transition-all"
          >
            Inspect
          </button>
        ),
      },
    ],
    []
  );

  if (loading) {
    return (
      <div className="text-white p-8 flex items-center justify-center min-h-[50vh]">
        <span className="font-header text-2xl uppercase tracking-wider text-gray-400 animate-pulse">
          Loading Front Office...
        </span>
      </div>
    );
  }

  const positions: PositionFilter[] = [
    "ALL",
    "OFF",
    "DEF",
    "QB",
    "RB",
    "WR",
    "TE",
    "OL",
    "DL",
    "LB",
    "DB",
    "K/P",
  ];

  return (
    <div className="space-y-6 font-body" data-testid="front-office-page">
      {/* Header Banner */}
      <header
        className="relative rounded-lg overflow-hidden bg-slate-950/80 backdrop-blur-xl p-6 border border-white/10 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4"
        data-testid="front-office-header"
      >
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-md bg-black/60 border border-white/15 p-2 shadow-xl flex items-center justify-center shrink-0">
            <img
              src={`/logos/${activeTeam?.abbreviation || team?.abbreviation || "GB"}.png`}
              alt={team?.name || "Team"}
              className="w-full h-full object-contain filter drop-shadow"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).style.display = "none";
              }}
            />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-emerald-400">
                Active 53-Man Franchise Roster
              </span>
            </div>
            <h1 className="text-3xl md:text-5xl font-header uppercase tracking-tight text-white leading-none mt-0.5">
              Front Office: {team?.city} {team?.name}
            </h1>
            <p className="text-gray-400 text-xs font-mono mt-1">
              General Manager & Head Coach Roster Management
            </p>
          </div>
        </div>

        {/* Cap Space & Health Vitals */}
        <div className="flex items-center gap-4 bg-black/50 backdrop-blur-md px-4 py-3 rounded-md border border-white/10">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest flex items-center gap-1 font-mono">
              <DollarSign size={12} className="text-emerald-400" /> Cap Room
            </span>
            <span className="font-header text-2xl text-emerald-400 leading-none mt-0.5">
              $12.4M
            </span>
          </div>

          <div className="h-8 w-[1px] bg-white/15" />

          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest flex items-center gap-1 font-mono">
              <Users size={12} className="text-yellow-400" /> Roster
            </span>
            <span className="font-header text-2xl text-white leading-none mt-0.5">
              {roster.length} / 53
            </span>
          </div>
        </div>
      </header>

      {/* Position Filter, Sort & Tri-Mode Spatial Controller Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-950/80 backdrop-blur-md p-3 rounded-lg border border-white/10 shadow-lg">
        {/* Position Filter Tabs */}
        <div className="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          <span className="text-xs font-mono text-gray-400 mr-1 flex items-center gap-1">
            <Filter size={12} /> Unit:
          </span>
          {positions.map((pos) => (
            <button
              key={pos}
              data-testid={`filter-${pos.toLowerCase()}`}
              onClick={() => {
                soundEffects.playSnap?.();
                setPositionFilter(pos);
              }}
              className={`px-3 py-1 rounded-md text-xs font-header uppercase tracking-wider transition-all duration-150 ${
                positionFilter === pos
                  ? "bg-gradient-to-r from-[#0076B6] to-[#005582] text-white font-bold shadow-md shadow-[#0076B6]/30 border border-[#0076B6]/50"
                  : "bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white border border-white/5"
              }`}
            >
              {pos}
            </button>
          ))}
        </div>

        {/* Sort & Tri-Mode Spatial Controller */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="text-gray-400 flex items-center gap-1">
              <ArrowUpDown size={12} /> Sort:
            </span>
            {(["OVR", "AGE", "SPEED", "STRENGTH"] as SortOption[]).map((opt) => (
              <button
                key={opt}
                onClick={() => {
                  soundEffects.playSnap?.();
                  setSortBy(opt);
                }}
                className={`px-2.5 py-1 rounded-md transition-colors ${
                  sortBy === opt
                    ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 font-bold"
                    : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
                }`}
              >
                {opt}
              </button>
            ))}
          </div>

          {/* Tri-Mode Spatial Controller Switcher */}
          <div className="flex items-center bg-black/60 p-1 rounded-md border border-white/10 gap-1">
            <button
              data-testid="mode-toggle-lockers"
              onClick={() => handleModeChange("lockers")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-header uppercase tracking-wider transition-all duration-150 ${
                mode === "lockers"
                  ? "bg-gradient-to-r from-[#0076B6] to-[#005582] text-white font-bold shadow-md shadow-[#0076B6]/30 border border-[#0076B6]/50"
                  : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
              }`}
              title="Spatial Lockers (Ford Field Honolulu Blue Viewport)"
            >
              <Shield
                size={13}
                className={mode === "lockers" ? "text-cyan-300" : "text-gray-400"}
              />
              <span>Spatial Lockers</span>
            </button>

            <button
              data-testid="mode-toggle-office"
              onClick={() => handleModeChange("office")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-header uppercase tracking-wider transition-all duration-150 ${
                mode === "office"
                  ? "bg-gradient-to-r from-[#0076B6] to-[#005582] text-white font-bold shadow-md shadow-[#0076B6]/30 border border-[#0076B6]/50"
                  : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
              }`}
              title="Coach Office (Dan Campbell's Executive Corner Office)"
            >
              <ClipboardList
                size={13}
                className={mode === "office" ? "text-cyan-300" : "text-gray-400"}
              />
              <span>Coach Office</span>
            </button>

            <button
              data-testid="mode-toggle-table"
              onClick={() => handleModeChange("table")}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-header uppercase tracking-wider transition-all duration-150 ${
                mode === "table"
                  ? "bg-gradient-to-r from-[#0076B6] to-[#005582] text-white font-bold shadow-md shadow-[#0076B6]/30 border border-[#0076B6]/50"
                  : "text-gray-400 hover:text-white hover:bg-white/5 border border-transparent"
              }`}
              title="Tactical Table (Virtualized Monograph Ledger)"
            >
              <TableIcon
                size={13}
                className={mode === "table" ? "text-cyan-300" : "text-gray-400"}
              />
              <span>Tactical Table</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Mode Viewport Projections */}

      {/* 1. SPATIAL LOCKERS: Ford Field Honolulu Blue Player Locker Stalls */}
      {mode === "lockers" && (
        <SpatialSceneViewport
          backgroundSrc="/assets/spatial/ford_field_locker_roster_1789187061053.jpg"
          atmosphereType="locker"
          overscan={1.06}
          parallaxBounds={LOCKER_PARALLAX}
          className="min-h-[calc(100vh-220px)] rounded-lg overflow-hidden border border-white/10 p-4 sm:p-6"
        >
          {/* Subtle Locker Atmosphere Mist Overlay */}
          <SpatialAtmosphereLayer facilityType="locker" intensity="subtle" />
          {/* Locker Room Ambient Header */}
          <div className="mb-6 bg-slate-950/80 backdrop-blur-xl border border-white/10 p-5 rounded-lg shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-md bg-black/60 border border-[#0076B6]/40 flex items-center justify-center p-2 text-[#0076B6] shadow-[0_0_16px_rgba(0,118,182,0.3)]">
                <Shield size={24} />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
                  <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-cyan-400">
                    Ford Field First-Person Locker Room
                  </span>
                </div>
                <h2 className="text-xl md:text-2xl font-header uppercase tracking-tight text-white leading-tight">
                  Honolulu Blue & Silver 53-Man Stall Matrix
                </h2>
                <p className="text-gray-400 text-xs font-mono mt-0.5">
                  First-Person Player Lockers with Metallic Nameplates & Biometric Dossiers
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-xs font-mono px-3 py-1.5 rounded-md bg-[#0076B6]/20 border border-[#0076B6]/40 text-cyan-300 font-bold uppercase tracking-wider">
                Active Roster: {filteredAndSortedRoster.length} / 53
              </span>
            </div>
          </div>

          {/* Active Roster Locker Grid Container */}
          <div
            className="bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-lg p-6 shadow-2xl"
            data-testid="roster-section"
          >
            <div className="flex justify-between items-center mb-5 pb-3 border-b border-white/10">
              <h2 className="font-header text-2xl uppercase tracking-wider text-white flex items-center gap-2">
                <Users size={20} className="text-yellow-400" />
                Active Roster ({filteredAndSortedRoster.length})
              </h2>
              <span className="text-xs font-mono text-gray-400">
                Click locker stall or nameplate to inspect dossier
              </span>
            </div>

            <div
              data-testid="roster-grid"
              className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-5 max-h-[720px] overflow-y-auto pr-2 custom-scrollbar"
            >
              {filteredAndSortedRoster.map((player) => (
                <LockerStallCard
                  key={player.id}
                  player={player}
                  teamAbbr={team?.abbreviation || activeTeam?.abbreviation || "DET"}
                  onClick={() => {
                    soundEffects.playSnap?.();
                    setSelectedPlayer(player);
                  }}
                />
              ))}
            </div>
          </div>
        </SpatialSceneViewport>
      )}

      {/* 2. COACH OFFICE: Dan Campbell Executive Corner Office Framing */}
      {mode === "office" && (
        <SpatialSceneViewport
          backgroundSrc="/assets/spatial/dan_campbell_office_1789188197446.jpg"
          atmosphereType="office"
          overscan={1.06}
          parallaxBounds={OFFICE_PARALLAX}
          className="min-h-[calc(100vh-220px)] rounded-lg overflow-hidden border border-white/10 p-4 sm:p-6"
        >
          {/* Subtle Office Daylight and Ambient Overlay */}
          <SpatialAtmosphereLayer facilityType="office" intensity="subtle" />
          {/* Dan Campbell Executive Office Header Banner */}
          <div className="mb-6 bg-slate-950/80 backdrop-blur-xl border border-white/10 p-5 rounded-lg shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-md bg-black/60 border border-white/10 flex items-center justify-center p-2 text-cyan-400">
                <ClipboardList size={24} />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-cyan-400">
                    Executive Corner Office • Allen Park HQ
                  </span>
                </div>
                <h2 className="text-xl md:text-2xl font-header uppercase tracking-tight text-white leading-tight">
                  Dan Campbell Coaching Command & Tactical Tendencies
                </h2>
                <p className="text-gray-400 text-xs font-mono mt-0.5">
                  "We're going to bite a kneecap off, and when we stand up, we're going to take
                  another one."
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="px-3 py-1.5 rounded-md bg-[#0076B6]/20 border border-[#0076B6]/40 text-cyan-300 font-mono text-xs font-bold uppercase tracking-wider">
                Culture: 100% Grit
              </div>
              <div className="px-3 py-1.5 rounded-md bg-amber-500/20 border border-amber-500/40 text-amber-300 font-mono text-xs font-bold uppercase tracking-wider">
                4th Down Rate: 88%
              </div>
            </div>
          </div>

          {/* Main Grid: Tactical Tendencies & CoachSettings (8 cols) + Side Active Roster (4 cols) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Left 8 Cols: Coach Settings & Tactical Directives */}
            <div className="lg:col-span-8 space-y-6">
              {/* Dan Campbell Dynamic Tactical Whiteboard */}
              <DanCampbellWhiteboard
                opponentName={
                  activeTeam?.abbreviation === "KC" ? "SAN FRANCISCO 49ERS" : "KANSAS CITY CHIEFS"
                }
                week={5}
              />

              {/* Tactical Tendency Briefing Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-lg p-4 shadow-xl">
                  <div className="flex items-center gap-2 text-amber-400 font-header text-sm uppercase mb-2">
                    <Shield size={16} /> 4th-Down Aggression
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed font-body">
                    Hyper-aggressive conversion mentality. Green light on 4th & 3 or less across
                    midfield.
                  </p>
                  <div className="mt-3 text-[10px] font-mono text-emerald-400 uppercase font-bold">
                    League Rank: #1 Aggressive
                  </div>
                </div>

                <div className="bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-lg p-4 shadow-xl">
                  <div className="flex items-center gap-2 text-cyan-400 font-header text-sm uppercase mb-2">
                    <ClipboardList size={16} /> Power Run & Play-Action
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed font-body">
                    Heavy 12/13 personnel, pulling interior guards, explosive deep shot post
                    play-action.
                  </p>
                  <div className="mt-3 text-[10px] font-mono text-cyan-400 uppercase font-bold">
                    Run-Pass Split: 54% / 46%
                  </div>
                </div>

                <div className="bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-lg p-4 shadow-xl">
                  <div className="flex items-center gap-2 text-purple-400 font-header text-sm uppercase mb-2">
                    <Award size={16} /> Defensive Front Havoc
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed font-body">
                    Attacking A-gap mug fronts, 5-man disguised creepers, tight press-man on
                    boundary.
                  </p>
                  <div className="mt-3 text-[10px] font-mono text-purple-400 uppercase font-bold">
                    Blitz Frequency: 38.5%
                  </div>
                </div>
              </div>

              {/* Embedded CoachSettings Component */}
              {team && (
                <div className="bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-lg p-6 shadow-2xl">
                  <div className="border-b border-white/10 pb-3 mb-4">
                    <h3 className="font-header text-xl uppercase tracking-wider text-white">
                      Tactical Playcalling & Gameplan Sliders
                    </h3>
                    <p className="text-xs font-mono text-gray-400">
                      Configure offensive tempo, red-zone strategy, and defensive coverage shell
                    </p>
                  </div>
                  <CoachSettings
                    teamId={team.id}
                    onTacticalTick={() => soundEffects.playTacticalTick()}
                  />
                </div>
              )}
            </div>

            {/* Right 4 Cols: Tactical Roster Depth Sheet with Critical Selectors */}
            <div
              className="lg:col-span-4 bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-lg p-5 shadow-2xl flex flex-col"
              data-testid="roster-section"
            >
              <div className="flex justify-between items-center mb-4 pb-3 border-b border-white/10">
                <h2 className="font-header text-lg uppercase tracking-wider text-white flex items-center gap-2">
                  <Users size={18} className="text-yellow-400" />
                  Active Roster ({filteredAndSortedRoster.length})
                </h2>
                <span className="text-[10px] font-mono text-cyan-300">Staff Sheet</span>
              </div>

              <div
                data-testid="roster-grid"
                className="space-y-2.5 max-h-[640px] overflow-y-auto pr-1 custom-scrollbar"
              >
                {filteredAndSortedRoster.map((player) => (
                  <div
                    key={player.id}
                    data-testid={`player-card-${player.id}`}
                    role="button"
                    tabIndex={0}
                    onClick={() => {
                      soundEffects.playSnap?.();
                      setSelectedPlayer(player);
                    }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" || e.key === " ") {
                        e.preventDefault();
                        setSelectedPlayer(player);
                      }
                    }}
                    className="group flex items-center justify-between p-3 rounded-md border border-white/10 hover:border-[#0076B6] bg-black/40 hover:bg-[#0076B6]/10 transition-all duration-150 cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#0076B6]"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <span className="font-header text-sm text-yellow-400 font-bold shrink-0">
                        #{player.jersey_number ?? 0}
                      </span>
                      <div className="min-w-0">
                        <p className="font-header text-sm text-white uppercase truncate group-hover:text-cyan-300 transition-colors">
                          {player.first_name} {player.last_name}
                        </p>
                        <span className="text-[10px] font-mono text-gray-400">
                          {player.position} • {player.age} yo
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <div className="px-2 py-0.5 rounded bg-white/10 font-header text-sm text-white font-bold">
                        {player.overall_rating}
                      </div>
                      <span className="text-xs font-mono text-cyan-400 group-hover:translate-x-0.5 transition-transform">
                        &rarr;
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </SpatialSceneViewport>
      )}

      {/* 3. TACTICAL TABLE: Direct 2D Virtualized Monograph Ledger */}
      {mode === "table" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div
            className="lg:col-span-2 bg-slate-950/90 border border-white/10 rounded-lg p-6 shadow-2xl flex flex-col min-h-[560px]"
            data-testid="roster-section"
          >
            <div className="flex justify-between items-center mb-4 pb-3 border-b border-white/10">
              <div>
                <h2 className="font-header text-2xl uppercase tracking-wider text-white flex items-center gap-2">
                  <TableIcon size={20} className="text-cyan-400" />
                  Active Roster ({filteredAndSortedRoster.length})
                </h2>
                <p className="text-xs font-mono text-gray-400 mt-0.5">
                  High-Density Tactical Personnel Ledger • Virtualized 60 FPS
                </p>
              </div>
              <span className="text-xs font-mono px-2.5 py-1 rounded bg-white/5 border border-white/10 text-gray-300">
                Click row to inspect dossier
              </span>
            </div>

            <div data-testid="roster-grid" className="flex-1">
              <VirtualizedTable
                data={filteredAndSortedRoster}
                columns={tableColumns}
                height={560}
                estimateRowHeight={50}
                overscan={12}
                getRowId={(player) => player.id}
                onRowClick={(player) => {
                  soundEffects.playSnap?.();
                  setSelectedPlayer(player);
                }}
                emptyMessage="No players found in this unit filter."
                testId="virtualized-roster-table"
              />
            </div>
          </div>

          {/* Coach Settings Sidebar */}
          {team && (
            <div className="lg:col-span-1 bg-slate-950/90 border border-white/10 rounded-lg p-6 shadow-2xl">
              <CoachSettings teamId={team.id} />
            </div>
          )}
        </div>
      )}

      {/* Detailed Player Modal */}
      {selectedPlayer && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4"
          data-testid="player-modal"
          onClick={() => setSelectedPlayer(null)}
        >
          <div
            className="bg-slate-950/95 border border-white/20 rounded-lg p-6 max-w-lg w-full relative shadow-2xl backdrop-blur-xl"
            data-testid="player-modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setSelectedPlayer(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white p-1.5 rounded-md bg-white/5 hover:bg-white/10 transition-colors focus:outline-none focus:ring-1 focus:ring-white/20"
              aria-label="Close player details"
              data-testid="close-modal-button"
            >
              <X size={18} />
            </button>

            {/* Header */}
            <div className="flex items-center gap-4 mb-6 pb-4 border-b border-white/10">
              <div className="w-16 h-16 rounded-md bg-black/60 border border-white/20 flex items-center justify-center shadow-lg">
                <span className="font-header text-3xl text-yellow-400">
                  #{selectedPlayer.jersey_number ?? 0}
                </span>
              </div>
              <div>
                <h2 className="font-header text-3xl text-white uppercase leading-tight">
                  {selectedPlayer.first_name} {selectedPlayer.last_name}
                </h2>
                <p className="text-sm font-mono text-gray-300">
                  {selectedPlayer.position} • {team?.name}
                </p>
              </div>
            </div>

            {/* Attribute Grid */}
            <div className="grid grid-cols-2 gap-3 mb-6">
              <div className="bg-black/40 p-3 rounded-md border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Overall Rating
                </p>
                <p className="text-3xl font-header text-yellow-400">
                  {selectedPlayer.overall_rating}
                </p>
              </div>

              <div className="bg-black/40 p-3 rounded-md border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Age
                </p>
                <p className="text-3xl font-header text-white">{selectedPlayer.age}</p>
              </div>

              <div className="bg-black/40 p-3 rounded-md border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Speed
                </p>
                <p className="text-2xl font-header text-emerald-400" data-testid="player-speed">
                  {selectedPlayer.speed ?? 85}
                </p>
              </div>

              <div className="bg-black/40 p-3 rounded-md border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Strength
                </p>
                <p className="text-2xl font-header text-cyan-400" data-testid="player-strength">
                  {selectedPlayer.strength ?? 80}
                </p>
              </div>
            </div>

            {/* Full Attributes Breakdown Bar */}
            <div className="space-y-2 pt-2 border-t border-white/10 text-xs font-mono">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Agility:</span>
                <span className="text-white font-bold">{selectedPlayer.agility ?? 84}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Experience:</span>
                <span className="text-white font-bold">{selectedPlayer.experience ?? 3} yrs</span>
              </div>
            </div>

            {/* Traits Section if available */}
            {(selectedPlayer as any).traits && (selectedPlayer as any).traits.length > 0 && (
              <div
                className="mt-4 pt-3 border-t border-white/10 traits-section"
                data-testid="player-traits"
              >
                <p className="text-[10px] uppercase font-mono tracking-wider text-gray-400 mb-1.5">
                  Player Traits
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {(selectedPlayer as any).traits.map((trait: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded bg-white/5 border border-white/10 text-xs font-mono text-cyan-300"
                    >
                      {trait}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Contract Section if available */}
            {(selectedPlayer as any).contract && (
              <div
                className="mt-3 pt-3 border-t border-white/10 contract-info"
                data-testid="player-contract"
              >
                <p className="text-[10px] uppercase font-mono tracking-wider text-gray-400 mb-1">
                  Contract Terms
                </p>
                <p className="text-xs font-mono text-emerald-400 font-bold">
                  {(selectedPlayer as any).contract.salary || "$45M / 3 Yrs"}
                </p>
              </div>
            )}

            {/* Authentic Equipment Loadout Panel */}
            <div
              className="mt-4 pt-3 border-t border-white/10"
              data-testid="player-equipment-loadout"
            >
              <div className="flex items-center justify-between mb-2">
                <p className="text-[10px] uppercase font-mono tracking-wider text-gray-400 flex items-center gap-1.5 font-bold">
                  <Shield size={12} className="text-[#0076B6]" />
                  Gameday Equipment Loadout
                </p>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 uppercase font-bold">
                  NFL Certified
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2.5 text-xs font-mono">
                {/* 1. Helmet & Visor */}
                <div className="p-2.5 rounded bg-black/50 border border-white/10 flex flex-col justify-between">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[9px] text-gray-400 uppercase font-bold">
                      Helmet &amp; Visor
                    </span>
                    <span
                      className="w-2.5 h-2.5 rounded-full border border-white/20 shadow-sm shrink-0"
                      style={{
                        backgroundColor:
                          activeTeam?.colors?.primary || team?.primary_color || "#0076B6",
                      }}
                      title="Team Shell Color"
                    />
                  </div>
                  <p className="text-white font-semibold text-[11px] truncate">
                    Riddell SpeedFlex Precision
                  </p>
                  <p className="text-cyan-400 text-[10px] mt-0.5">
                    Visor:{" "}
                    {["QB", "K", "P"].includes(selectedPlayer.position)
                      ? "Clear High-Def Shield"
                      : "Smoke Iridium 20% Tint"}
                  </p>
                </div>

                {/* 2. Gloves */}
                <div className="p-2.5 rounded bg-black/50 border border-white/10 flex flex-col justify-between">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[9px] text-gray-400 uppercase font-bold">
                      Grip Gloves
                    </span>
                    <span
                      className="w-2.5 h-2.5 rounded-full border border-white/20 shadow-sm shrink-0"
                      style={{
                        backgroundColor:
                          activeTeam?.colors?.secondary || team?.secondary_color || "#B0B7BC",
                      }}
                      title="Team Accent Color"
                    />
                  </div>
                  <p className="text-white font-semibold text-[11px] truncate">
                    Nike Vapor Jet 7.0
                  </p>
                  <p className="text-amber-400 text-[10px] mt-0.5">Magnigrip+ Tack &bull; Strap</p>
                </div>

                {/* 3. Jersey Loadout */}
                <div className="p-2.5 rounded bg-black/50 border border-white/10 flex flex-col justify-between">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[9px] text-gray-400 uppercase font-bold">
                      Jersey Loadout
                    </span>
                    <span className="text-[11px] font-header text-yellow-400 font-bold leading-none">
                      #{selectedPlayer.jersey_number ?? 0}
                    </span>
                  </div>
                  <p className="text-white font-semibold text-[11px] truncate">
                    Nike Vapor F.U.S.E. Mesh
                  </p>
                  <p className="text-gray-300 text-[10px] mt-0.5">Douglas CP 25 Pro Kevlar</p>
                </div>

                {/* 4. Cleats & Spatting */}
                <div className="p-2.5 rounded bg-black/50 border border-white/10 flex flex-col justify-between">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[9px] text-gray-400 uppercase font-bold">
                      Cleats &amp; Spatting
                    </span>
                    <span className="text-[9px] text-emerald-400 font-bold">Molded</span>
                  </div>
                  <p className="text-white font-semibold text-[11px] truncate">
                    Nike Vapor Edge Pro 360
                  </p>
                  <p className="text-cyan-300 text-[10px] mt-0.5">Carbon Plate &bull; Turf Tape</p>
                </div>
              </div>
            </div>

            <button
              onClick={() => {
                setEnhancedPlayerId(selectedPlayer.id);
                setSelectedPlayer(null);
              }}
              className="w-full mt-5 py-2.5 bg-gradient-to-r from-[#0076B6] to-blue-700 hover:from-cyan-600 hover:to-blue-600 text-white font-header text-sm uppercase tracking-wider rounded-md shadow-lg transition-all focus:outline-none focus:ring-1 focus:ring-cyan-400"
            >
              Open In-Depth Biometrics & Traits Dossier
            </button>
          </div>
        </div>
      )}

      {/* In-Depth Enhanced Player Profile Modal */}
      {enhancedPlayerId && (
        <EnhancedPlayerProfile
          playerId={enhancedPlayerId}
          onClose={() => setEnhancedPlayerId(null)}
        />
      )}
    </div>
  );
};

export default FrontOffice;
