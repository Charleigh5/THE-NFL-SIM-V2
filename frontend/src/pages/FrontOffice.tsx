import { useEffect, useState } from "react";
import { DraggableCard } from "../components/ui/DraggableCard";
import { api } from "../services/api";
import type { Player, Team } from "../services/api";

export const FrontOffice = () => {
  const [roster, setRoster] = useState<Player[]>([]);
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
              />
            ))}
          </div>
        </div>
        <div className="glass-panel p-6 rounded-xl border border-white/5 min-h-[500px] flex items-center justify-center">
          <span className="text-white/20 font-mono">TRANSACTION_LOG</span>
        </div>
      </div>
    </div>
  );
};
