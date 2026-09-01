import { useEffect, useState, useMemo } from "react";
import { DraggableCard } from "../components/ui/DraggableCard";
import { EnhancedPlayerProfile } from "../components/ui/EnhancedPlayerProfile";
import CoachSettings from "../components/coaching/CoachSettings";
import { api } from "../services/api";
import { useTheme } from "../context/useTheme";
import { soundEffects } from "../services/soundEffects";
import type { Player, Team } from "../services/api";
import { Users, Filter, ArrowUpDown, DollarSign, X } from "lucide-react";

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

export const FrontOffice = () => {
  const [roster, setRoster] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [enhancedPlayerId, setEnhancedPlayerId] = useState<number | null>(null);
  const [team, setTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [positionFilter, setPositionFilter] = useState<PositionFilter>("ALL");
  const [sortBy, setSortBy] = useState<SortOption>("OVR");
  const { activeTeam } = useTheme();

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

  if (loading) {
    return (
      <div className="text-white p-8 flex items-center justify-center min-h-[50vh]">
        <span className="font-header text-2xl uppercase tracking-wider text-gray-400 animate-pulse">
          Loading Franchise Roster...
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
        className="relative rounded-2xl overflow-hidden broadcast-glass p-6 border border-white/15 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4"
        data-testid="front-office-header"
      >
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-xl bg-black/60 border-2 border-white/15 p-2 shadow-xl flex items-center justify-center shrink-0">
            <img
              src={`/logos/${activeTeam?.abbreviation || "GB"}.png`}
              alt={team?.name || "Team"}
              className="w-full h-full object-contain filter drop-shadow"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).style.display = "none";
              }}
            />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
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
        <div className="flex items-center gap-4 bg-black/40 backdrop-blur-md px-4 py-3 rounded-xl border border-white/10">
          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest flex items-center gap-1">
              <DollarSign size={12} className="text-emerald-400" /> Cap Room
            </span>
            <span className="font-header text-2xl text-emerald-400 leading-none mt-0.5">
              $12.4M
            </span>
          </div>

          <div className="h-8 w-[1px] bg-white/15" />

          <div className="flex flex-col">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest flex items-center gap-1">
              <Users size={12} className="text-yellow-400" /> Roster
            </span>
            <span className="font-header text-2xl text-white leading-none mt-0.5">
              {roster.length} / 53
            </span>
          </div>
        </div>
      </header>

      {/* Position Filter & Sort Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-broadcast-dark/80 backdrop-blur-md p-3 rounded-xl border border-white/10 shadow-lg">
        {/* Position Filter Tabs */}
        <div className="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          <span className="text-xs font-mono text-gray-400 mr-1 flex items-center gap-1">
            <Filter size={12} /> Unit:
          </span>
          {positions.map((pos) => (
            <button
              key={pos}
              onClick={() => {
                soundEffects.playSnap();
                setPositionFilter(pos);
              }}
              className={`px-3 py-1 rounded-md text-xs font-header uppercase tracking-wider transition-all ${
                positionFilter === pos
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-md shadow-red-600/30"
                  : "bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white"
              }`}
            >
              {pos}
            </button>
          ))}
        </div>

        {/* Sort Selector */}
        <div className="flex items-center gap-2 text-xs font-mono">
          <span className="text-gray-400 flex items-center gap-1">
            <ArrowUpDown size={12} /> Sort:
          </span>
          {(["OVR", "AGE", "SPEED", "STRENGTH"] as SortOption[]).map((opt) => (
            <button
              key={opt}
              onClick={() => {
                soundEffects.playSnap();
                setSortBy(opt);
              }}
              className={`px-2.5 py-1 rounded transition-colors ${
                sortBy === opt
                  ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 font-bold"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Main Roster Deck & Coach Settings */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div
          className="lg:col-span-2 broadcast-glass p-6 rounded-2xl border border-white/15 min-h-[500px] shadow-2xl"
          data-testid="roster-section"
        >
          <div className="flex justify-between items-center mb-5 pb-3 border-b border-white/10">
            <h2 className="font-header text-2xl uppercase tracking-wider text-white flex items-center gap-2">
              <Users size={20} className="text-yellow-400" />
              Active Roster ({filteredAndSortedRoster.length})
            </h2>
            <span className="text-xs font-mono text-gray-400">
              Click athlete to inspect attributes
            </span>
          </div>

          <div
            className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4 max-h-[640px] overflow-y-auto pr-2 custom-scrollbar"
            data-testid="roster-grid"
          >
            {filteredAndSortedRoster.map((player) => (
              <DraggableCard
                key={player.id}
                playerId={player.id}
                name={`${player.first_name.charAt(0)}. ${player.last_name}`}
                position={player.position}
                rating={player.overall_rating}
                team={team?.abbreviation || "UNK"}
                jerseyNumber={player.jersey_number}
                speed={player.speed || 85}
                strength={player.strength || 80}
                agility={player.agility || 84}
                onClick={() => setSelectedPlayer(player)}
                testId={`player-card-${player.id}`}
              />
            ))}
          </div>
        </div>

        {/* Coach Settings Sidebar */}
        {team && (
          <div className="lg:col-span-1 broadcast-glass p-6 rounded-2xl border border-white/15 shadow-2xl">
            <CoachSettings teamId={team.id} />
          </div>
        )}
      </div>

      {/* Detailed Player Modal */}
      {selectedPlayer && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4"
          data-testid="player-modal"
          onClick={() => setSelectedPlayer(null)}
        >
          <div
            className="broadcast-glass rounded-2xl border border-white/20 p-6 max-w-lg w-full relative shadow-2xl"
            data-testid="player-modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setSelectedPlayer(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white p-1 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
              aria-label="Close player details"
              data-testid="close-modal-button"
            >
              <X size={20} />
            </button>

            {/* Header */}
            <div className="flex items-center gap-4 mb-6 pb-4 border-b border-white/10">
              <div className="w-16 h-16 rounded-xl bg-black/60 border-2 border-white/20 flex items-center justify-center shadow-lg">
                <span className="font-header text-3xl text-yellow-400">
                  #{selectedPlayer.jersey_number || 0}
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
              <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Overall Rating
                </p>
                <p className="text-3xl font-header text-yellow-400">
                  {selectedPlayer.overall_rating}
                </p>
              </div>

              <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Age
                </p>
                <p className="text-3xl font-header text-white">{selectedPlayer.age}</p>
              </div>

              <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                <p className="text-gray-400 text-[10px] uppercase font-mono tracking-wider mb-0.5">
                  Speed
                </p>
                <p className="text-2xl font-header text-emerald-400" data-testid="player-speed">
                  {selectedPlayer.speed ?? 85}
                </p>
              </div>

              <div className="bg-black/40 p-3 rounded-xl border border-white/5">
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

            <button
              onClick={() => {
                setEnhancedPlayerId(selectedPlayer.id);
                setSelectedPlayer(null);
              }}
              className="w-full mt-4 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-header text-sm uppercase tracking-wider rounded-xl shadow-lg transition-all"
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
