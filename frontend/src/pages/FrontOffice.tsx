import { useEffect, useState } from "react";
import { DraggableCard } from "../components/ui/DraggableCard";
import { api } from "../services/api";
import type { Player, Team } from "../services/api";

export const FrontOffice = () => {
  const [roster, setRoster] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [team, setTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetching Team ID 1 (Arizona Cardinals) for demo
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

  if (loading) {
    return <div className="text-white p-6">Loading Front Office...</div>;
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-4xl font-bold text-white tracking-tight">
          Front Office: {team?.city} {team?.name}
        </h1>
        <p className="text-cyan-400/80">Cap Space: $12.4M</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel p-6 rounded-xl border border-white/5 min-h-[500px]">
          <h2 className="text-xl font-bold text-white mb-4">Active Roster ({roster.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 max-h-[600px] overflow-y-auto pr-2">
            {roster.map((player) => (
              <DraggableCard
                key={player.id}
                name={`${player.first_name.charAt(0)}. ${player.last_name}`}
                position={player.position}
                rating={player.overall_rating}
                team={team?.abbreviation || "UNK"}
                onClick={() => setSelectedPlayer(player)}
              />
            ))}
          </div>
        </div>
        <div className="glass-panel p-6 rounded-xl border border-white/5 min-h-[500px] flex items-center justify-center">
          <span className="text-white/20 font-mono">TRANSACTION_LOG</span>
        </div>
      </div>

      {/* Player Detail Modal */}
      {selectedPlayer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" data-testid="player-modal">
          <div className="bg-slate-900 border border-white/10 rounded-xl p-6 max-w-md w-full relative shadow-2xl">
            <button 
              onClick={() => setSelectedPlayer(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 18 18"/></svg>
            </button>
            
            <div className="flex items-center gap-4 mb-6">
              <div className="h-16 w-16 bg-gradient-to-br from-cyan-900 to-slate-800 rounded-full flex items-center justify-center border border-white/10">
                <span className="text-2xl font-bold text-cyan-400">{selectedPlayer.jersey_number}</span>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white leading-none mb-1">
                  {selectedPlayer.first_name} {selectedPlayer.last_name}
                </h2>
                <p className="text-cyan-400 font-medium">{selectedPlayer.position} • {team?.name}</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 p-4 rounded-lg border border-white/5">
                 <p className="text-gray-400 text-xs uppercase tracking-wider mb-1">Overall</p>
                 <p className="text-3xl font-mono font-bold text-white">{selectedPlayer.overall_rating}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg border border-white/5">
                 <p className="text-gray-400 text-xs uppercase tracking-wider mb-1">Age</p>
                 <p className="text-3xl font-mono font-bold text-white">{selectedPlayer.age}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg border border-white/5">
                 <p className="text-gray-400 text-xs uppercase tracking-wider mb-1">Speed</p>
                 <p className="text-2xl font-mono text-white" data-testid="player-speed">{selectedPlayer.speed ?? 'N/A'}</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg border border-white/5">
                 <p className="text-gray-400 text-xs uppercase tracking-wider mb-1">Strength</p>
                 <p className="text-2xl font-mono text-white" data-testid="player-strength">{selectedPlayer.strength ?? 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
